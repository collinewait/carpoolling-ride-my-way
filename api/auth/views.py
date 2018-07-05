"""
This module handles user account creation and
user authentication
"""
import uuid
from flask import request, jsonify, make_response
from flask.views import MethodView
from werkzeug.security import generate_password_hash, check_password_hash
from api.models.user import User
from api.models.rides import  RidesHandler
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
        if request.content_type == 'application/json':

            keys = ("first_name", "last_name", "email_address",
                    "phone_number", "password")
            if not set(keys).issubset(set(request.json)):
                return RidesHandler.request_missing_fields()

            user_condition = [
                request.json["first_name"], request.json["last_name"],
                request.json["email_address"], request.json["phone_number"],
                request.json["password"]
            ]

            if not all(user_condition):
                return RidesHandler.fields_missing_info()

            public_id = str(uuid.uuid4)
            post_data = request.get_json()
            first_name = post_data['first_name']
            last_name = post_data['last_name']
            email_address = post_data['email_address']
            phone_number = post_data['phone_number']
            hashed_password = generate_password_hash(post_data['password'], method='sha256')

            query = """SELECT * FROM "user" WHERE "email_address" = %s"""
            user_turple = DbTransaction.retrieve_one(query, (email_address, ))

            if not user_turple:
                new_user = User(public_id, first_name, last_name,
                                email_address, phone_number, hashed_password)

                user_sql = """INSERT INTO "user"(public_id, first_name, last_name, email_address,
                 phone_number, password)
                VALUES(%s, %s, %s, %s, %s, %s);"""
                data = (new_user.public_id, new_user.first_name, new_user.last_name,
                        new_user.email_address, new_user.phone_number, new_user.password)
                DbTransaction.save(user_sql, data)
                return jsonify({'message': 'Successfully registered',
                                "user": new_user.__dict__}), 201
            return jsonify({"error_message": 'Failed, User already exists,' +
                                             'Please sign In'}), 400
        return jsonify({'error_message': 'Failed Content-type must be json'}), 400


class LoginUser(MethodView):
    """
    This class is responsible for signing in a user.
    """

    def post(self):
        """
        This method Logs a user in if the supplied credentials are correct.
        Uses Http basic authentication and it returns a token used to authenticate
        subsequent requests made to other routes.
        :return: token
        """
        post_data = request.get_json()

        if not post_data or not post_data['email_address'] or not post_data['password']:
            return jsonify({"status": "Missing email address or password",
                            'Message': 'All Login details required'}), 401

        query = """SELECT * FROM "user" WHERE "email_address" = %s"""
        user = DbTransaction.retrieve_one(query, (post_data['email_address'], ))

        if not user:
            return jsonify({"status": "Incorrect Email address",
                            'Message': 'Please enter valid Email address'}), 401
        if check_password_hash(user[6], post_data['password']):
            auth_token = User.encode_token(user[1])
            if auth_token:
                response = {
                    "status": "success",
                    "message": "Successfully logged in.",
                    "auth_token": auth_token.decode()
                }
                return make_response(jsonify(response)), 200
            response = {
                "status": "fail",
                "message": "Try again"
            }
            return make_response(jsonify(response)), 400

        return jsonify({"status": "Incorrect password",
                        'Message': 'Please enter correct password'}), 401
    