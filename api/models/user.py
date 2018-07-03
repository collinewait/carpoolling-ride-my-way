"""
This module is a ride model with its attributes
"""
import psycopg2
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
    def get_by_email(email_address):
        """
        This method filters a user by email address.
        :param email_address:
        :return: email_address or None
        """
        conn = None
        try:
            conn = DatabaseAccess.database_connection()
            cur = conn.cursor()
            cur.execute("""SELECT "email_address" FROM "user" WHERE "email_address" = %s""",
                        (email_address,))
            print("The email obtained")
            email = cur.fetchone()

            if email:
                print(email)
                print("row sent")
                return(email)
            return None
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
           print(error)
        finally:
            if conn is not None:
                conn.close()
