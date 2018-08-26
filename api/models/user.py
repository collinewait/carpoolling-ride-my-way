"""
This module is a ride model with its attributes
"""
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


    @staticmethod
    def decode_token(auth_token):
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

    @staticmethod
    def decode_failure(message):
        """
        This method returns an error message when an error is
        encounterd on decoding the token
        """
        return jsonify({"message": message}), 401

    @staticmethod
    def check_login_status(user_id):
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
