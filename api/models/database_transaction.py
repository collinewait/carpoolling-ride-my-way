"""
This module is responsible for database transactions.
"""

import psycopg2
from api.models.database_connection import DatabaseAccess


class DbTransaction(object):
    """
    This class is responsible for making different database
    transactions.
    - inserting data into the database tables
    - updating the data in the database tables
    - quering data in the database tables
    """

    @staticmethod
    def save(sql, data):
        """
        This module inserts the data into the database depending on the
        recieved sql command and the data.
        :param:sql
        :param:data
        """
        conn = None
        try:
            conn = DatabaseAccess.database_connection()
            cur = conn.cursor()
            cur.execute(sql, data)
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def retrieve_one(sql, data):
        """
        This module gets a single row from the database depending on the
        recieved sql command and the data.
        returns the row
        :param:sql
        :param:data
        :return:row
        """
        conn = None
        try:
            conn = DatabaseAccess.database_connection()
            cur = conn.cursor()
            cur.execute(sql, data)
            row = cur.fetchone()
            cur.close()

            if row:
                return row
            return None

        except (Exception, psycopg2.DatabaseError) as error:
           print(error)
        finally:
            if conn is not None:
                conn.close()
