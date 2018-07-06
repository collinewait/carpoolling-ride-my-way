"""
This module is a ride model with its attributes
"""
import datetime
import jwt


class User(object):
    """
    This class represents a User entity
    """
    def __init__(self, *args):
        self.first_name = args[0]
        self.last_name = args[1]
        self.email_address = args[2]
        self.phone_number = args[3]
        self.password = args[4]

    @staticmethod
    def encode_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        from api import APP
        try:
            token = jwt.encode({"user_id": user_id,
                                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
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
    