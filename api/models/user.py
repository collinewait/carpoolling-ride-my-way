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
        self.public_id = args[0]
        self.first_name = args[1]
        self.last_name = args[2]
        self.email_address = args[3]
        self.phone_number = args[4]
        self.password = args[5]

    @staticmethod
    def encode_token(public_id):
        """
        Generates the Auth Token
        :return: string
        """
        from api import APP
        try:
            token = jwt.encode({"public_id": public_id,
                                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                               APP.secret_key)
            return token
        except Exception as e:
            return e

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
            return {"public_id": token["public_id"],
                    "state": "Success"}
        except jwt.ExpiredSignatureError:
            return {"error_message": "Signature expired. Please log in again.",
                    "state": "Failure"}
        except jwt.InvalidTokenError:
            return {"error_message": "Invalid token. Please log in again.",
                    "state": "Failure"}
    