"""
This module is a ride model with its attributes
"""
import datetime
import psycopg2
import jwt
from api.models.database_connection import DatabaseAccess


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

    def save(self):
        """
        This method persists the user in the database
        :param user:
        """
        sql = """INSERT INTO "user"(public_id, first_name, last_name, email_address,
                 phone_number, password)
                VALUES(%s, %s, %s, %s, %s, %s);"""

        conn = None
        try:
            conn = DatabaseAccess.database_connection()
            cur = conn.cursor()
            cur.execute(sql, (self.public_id, self.first_name, self.last_name,
                              self.email_address, self.phone_number, self.password))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
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

    @staticmethod
    def get_user_by_email(email_address):
        """
        This method filters a user by email address.
        :param email_address:
        :return: email_address or None
        """
        conn = None
        try:
            conn = DatabaseAccess.database_connection()
            cur = conn.cursor()
            cur.execute("""SELECT * FROM "user" WHERE "email_address" = %s""",
                        (email_address,))
            user = cur.fetchone()

            if user:
                return(user)
            return None
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
           print(error)
        finally:
            if conn is not None:
                conn.close()
