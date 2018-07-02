"""
This module handles the database set up
"""
import psycopg2

class DatabaseAccess(object):
    """
    This class contains methods to create a database connection
    and database table creation
    """

    @staticmethod
    def databace_connection():
        """
        This method creates a connection to the databse
        "dbname='testdb' user='test123' host='localhost' password='test123' port='5432'"
        :retun: connection
        """
        connection = psycopg2.connect(
            "dbname='testdb' user='test123' host='localhost' password='test123' port='5432'"
        )
        print "connected to the database"
        return connection
