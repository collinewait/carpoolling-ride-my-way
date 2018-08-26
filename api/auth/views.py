"""
This module handles user account creation and
user authentication
"""
import re
from flask import request, jsonify
from flask.views import MethodView
from werkzeug.security import generate_password_hash, check_password_hash
from api.models.user import User
from api.models.database_transaction import DbTransaction


class RegisterUser(MethodView):
    """
    View function to register a user via the api
    """
    
    def post(self):
        """
        Register a user, generate their token and add them to the database
        :return: Json Response with the user`s token
        """
        post_data = request.get_json()

        if self.verify_user_on_signup(post_data)["status"] == "failure":
            return jsonify({
                "error_message": self.verify_user_on_signup(post_data)["error_message"]}), 400

        hashed_password = generate_password_hash(post_data['password'], method='sha256')

        query = """SELECT * FROM "user" WHERE "email_address" = %s"""
        user_turple = DbTransaction.retrieve_one(query, (post_data['email_address'], ))

        if not user_turple:
            new_user = User(post_data['first_name'], post_data['last_name'],
                            post_data['email_address'], post_data['phone_number'],
                            hashed_password)

            new_user.save_user()
            return jsonify({'message': 'Successfully registered',
                            "user": new_user.return_user_details()}), 201
        return jsonify({"error_message": 'Failed, User already exists,' +
                                         'Please sign In'}), 400

    @staticmethod
    def verify_user_on_signup(user_request):
        """
        This method verifies a user when creating an account
        If valid, it returns a success massage
        Else it returns an error message
        :param:user_response:
        :return:
        """
        if request.content_type == 'application/json':

            keys = ("first_name", "last_name", "email_address",
                    "phone_number", "password")
            if not set(keys).issubset(set(user_request)):
                return {"status": "failure",
                        "error_message": "Some fields are missing, all fields are required"}

            user_condition = [
                user_request["first_name"].strip(),
                user_request["last_name"].strip(),
                user_request["email_address"].strip(),
                user_request["phone_number"].strip(),
                user_request["password"].strip()
            ]

            if not all(user_condition):
                return {"status": "failure",
                        "error_message": "Some fields are not defined"}

            if re.match(r"[^@]+@[^@]+\.[^@]+", user_request["email_address"]):
                return {"status": "success",
                        "message": "valid details"}

            return {"status": "failure",
                    "error_message": "Missing or wrong email format"}
        return {"status": "failure",
                "error_message": "Failed Content-type must be json"}


class LoginUser(MethodView):
    """
    This class is responsible for signing in a user.
    """
    user = User()
    
    def post(self):
        """
        This method Logs a user in if the supplied credentials are correct.
        Genetes a token used to authenticate subsequent requests made to other routes.
        :return: token
        """
        post_data = request.get_json()
        requirement = [post_data['email_address'].strip(), post_data['password']]
        if not all(requirement):
            return jsonify({"status": "Missing email address or password",
                            'Message': 'All Login details required'}), 401

        query = """SELECT * FROM "user" WHERE "email_address" = %s"""
        user = DbTransaction.retrieve_one(query, (post_data['email_address'], ))
        verified_user = self.verify_user_on_login(user, post_data['password'])

        if verified_user["status"] == "failure":
            return jsonify({"message": verified_user["error_message"]}), 401
        self.update_user_status(True, user[0])
        return jsonify(verified_user), 200
   
    def verify_user_on_login(self, user, password):
        """
        This method verifies a user before having access to the system
        If valid, It returns a success message with a token
        Else it returns an error message
        :param:user: a tuple containing user information
        :return:
        """
        if not user:
            return {"status": "failure",
                    'error_message': 'Please enter valid Email address'}
        if check_password_hash(user[5], password):
            auth_token = self.user.encode_token(user[0])
            if auth_token:
                response = {"status": "success", "message": "Successfully logged in.",
                            "auth_token": auth_token.decode()
                           }
                return response
            response = {"status": "failure", "error_message": "Try again"}
            return response

        return {"status": "failure",
                'error_message': 'Please enter correct password'}

    @staticmethod
    def update_user_status(status, user_id):
        """
        This method updates a user login status when logged in to true
        and to false when a user logs out.
        """
        user_status_update_sql = """UPDATE "user" SET is_loggedin = %s
                    WHERE user_id = %s"""
        if status:
            edit_data = (True, user_id)
        else:
            edit_data = (False, user_id)
        DbTransaction.edit(user_status_update_sql, edit_data)
        if status:
            return None
        return {"status": "success",
                'message': 'You are logged out successfully'}


class Logout(MethodView):
    """
    This class logs out a user from the system
    """
    def post(self):
        """This method logs out a user"""
        token = request.headers.get('auth_token')
        if not token:
            return jsonify({"message": "Token is missing"}), 401

        decoded = User.decode_token(request.headers.get('auth_token'))
        if decoded["state"] == "Failure":
            return User.decode_failure(decoded["error_message"])
        if User.check_login_status(decoded["user_id"]):
            logout_info = LoginUser.update_user_status(False, decoded["user_id"])
            if logout_info["status"] == "success":
                return jsonify(logout_info), 200
            return jsonify({"status": "failure",
                            'error_message': 'Failed to logout'}), 200
        return jsonify({"message": "Please login"}), 401
