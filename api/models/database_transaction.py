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
        This method inserts the data into the database depending on the
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
        This method gets a single row from the database depending on the
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

            if row and not "":
                return row
            return None

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def retrieve_all(sql, data=None):
        """
        This method gets a single row from the database depending on the
        recieved sql command and the data.
        returns the row
        :param:sql
        :param:data
        :return:row
        """
        list_tuple = []
        conn = None
        try:
            conn = DatabaseAccess.database_connection()
            cur = conn.cursor()
            if data is not None:
                cur.execute(sql, data)
            else:
                cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                list_tuple.append(row)
            cur.close()
            return list_tuple
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def edit(sql, data):
        """
        This method edits the data into the database depending on the
        recieved sql command and the data.
        :param:sql
        :param:data
        """
        conn = None
        try:
            conn = DatabaseAccess.database_connection()
            cur = conn.cursor()
            cur.execute(sql, data)
            updated_rows = cur.rowcount
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return updated_rows
                