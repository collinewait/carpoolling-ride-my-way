"""
This module is a ride model with its attributes
"""
import re
import datetime
import jwt
from flask import jsonify
from api.models.database_transaction import DbTransaction


class User(object):
    """
    This class represents a User entity
    """
    def __init__(self, *args):
        if args:
            self.first_name = args[0]
            self.last_name = args[1]
            self.email_address = args[2]
            self.phone_number = args[3]
            self.password = args[4]

    def save_user(self):
        """
        This method saves a user instance in the database.
        """
        user_data = (self.first_name, self.last_name,
                     self.email_address, self.phone_number, self.password)
        user_sql = """INSERT INTO "user"(first_name, last_name, email_address,
            phone_number, password)
            VALUES(%s, %s, %s, %s, %s);"""
        DbTransaction.save(user_sql, user_data)

    def return_user_details(self):
        """
        This method returns the details of the user
        in json format.
        """ 
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email_address": self.email_address,
            "phone_number": self.phone_number
        }

    def verify_user_on_signup(self, user_request):
        """
        This method verifies a user when creating an account
        If valid, it returns a success massage
        Else it returns an e\rror message
        :param:user_response:
        :return:
        """
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

    def update_user_status(self, status, user_id):
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

    def encode_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        from api import APP
        try:
            token = jwt.encode({"user_id": user_id,
                                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=2880)},
                               APP.secret_key)
            return token
        except Exception as error:
            return error

    def decode_token(self, auth_token):
        """
        Decodes the auth token and returns the user public id
        :param auth_token:
        :return:
        """
        from api import APP
        try:
            token = jwt.decode(auth_token, APP.config.get("SECRET_KEY"))
            return {"user_id": token["user_id"],
                    "state": "Success"}
        except jwt.ExpiredSignatureError:
            return {"error_message": "Signature expired. Please log in again.",
                    "state": "Failure"}
        except jwt.InvalidTokenError:
            return {"error_message": "Invalid token. Please log in again.",
                    "state": "Failure"}

    def decode_failure(self, message):
        """
        This method returns an error message when an error is
        encounterd on decoding the token
        """
        return jsonify({"message": message}), 401

    def check_login_status(self, user_id):
        """
        This method checks whether a user is logged in or not
        If a user is logged in, it returns true and returns
        false if a user is not logged in
        :param user_id: User Id
        :return
        """
        is_loggedin = DbTransaction.retrieve_one(
            """SELECT "is_loggedin" FROM "user" WHERE "user_id" = %s""",
            (user_id, ))
        if is_loggedin[0]:
            return True
        return False
