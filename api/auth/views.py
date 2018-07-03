"""
This module handles user account creation and
user authentication
"""
import uuid
from flask import request, jsonify, make_response
from flask.views import MethodView
from werkzeug.security import generate_password_hash
from api.models.user import User
from api.models.rides import  RidesHandler


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

            user_public_id = User.get_public_id(public_id)

            if not user_public_id:
                new_user = User(public_id, first_name, last_name,
                                email_address, phone_number, hashed_password)
                User.save(new_user)
                return jsonify({'message': 'Successfully registered',
                                "user": new_user.__dict__}), 201
            return jsonify({"error_message": 'Failed, User already exists,' +
                                             'Please sign In'}), 400
        return jsonify({'error_message': 'Failed Content-type must be json'}), 400
