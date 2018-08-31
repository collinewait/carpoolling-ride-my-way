"""
This module handles user account creation and
user authentication
"""
from flask import request, jsonify
from flask.views import MethodView
from werkzeug.security import generate_password_hash, check_password_hash
from api.models.user import User
from api.models.database_transaction import DbTransaction


class RegisterUser(MethodView):
    """
    View function to register a user via the api
    """
    
    user_obj = User()

    def post(self):
        """
        Register a user, generate their token and add them to the database
        :return: Json Response with the user`s token
        """
        post_data = request.get_json()

        if request.content_type == 'application/json':
            if self.user_obj.verify_user_on_signup(post_data)["status"] == "failure":
                return jsonify({
                    "error_message": self.user_obj.verify_user_on_signup(post_data)["error_message"]}), 400

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
        return jsonify({"status": "failure",
                "error_message": "Failed Content-type must be json"}), 400


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
        self.user.update_user_status(True, user[0])
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


class Logout(MethodView):
    """
    This class logs out a user from the system
    """

    user_obj = User()

    def post(self):
        """This method logs out a user"""
        token = request.headers.get('auth_token')
        if not token:
            return jsonify({"message": "Token is missing"}), 401

        decoded = self.user_obj.decode_token(token)
        if decoded["state"] == "Failure":
            return self.user_obj.decode_failure(decoded["error_message"])
        if self.user_obj.check_login_status(decoded["user_id"]):
            logout_info = self.user_obj.update_user_status(False, decoded["user_id"])
            if logout_info["status"] == "success":
                return jsonify(logout_info), 200
            return jsonify({"status": "failure",
                            'error_message': 'Failed to logout'}), 200
        return jsonify({"message": "Please login"}), 401
