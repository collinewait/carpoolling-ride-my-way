"""
This module handles the database set up
"""
import os
import psycopg2

class DatabaseAccess(object):
    """
    This class contains methods to create a database connection
    and database table creation
    """
    @staticmethod
    def database_connection():
        """
        This method creates a connection to the databse
        "dbname='testdb' user='test123' host='localhost' password='test123' port='5432'"
        :retun: connection
        """
        from api import APP

        DATABASE_URL = os.environ['DATABASE_URL']

        if not APP.config['TESTING']:
            connection = psycopg2.connect(DATABASE_URL, sslmode='require')
            return connection
        connection = psycopg2.connect(
            "dbname='testdb' user='test123' host='localhost' password='test123' port='5432'"
        )
        return connection

    @staticmethod
    def create_tables(app):
        """
        This method creates tables in the PostgreSQL database.
        It conects to the databse and creates tables one by one
        for command in commands:
                cur.execute(command)
        """
        commands = (
            """
            CREATE TABLE "user" (
                    user_id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    email_address VARCHAR(50) UNIQUE NOT NULL,
                    phone_number INTEGER NOT NULL,
                    password VARCHAR(80) NOT NULL,
                    is_loggedin BOOLEAN DEFAULT FALSE
                )
            """,
            """
            CREATE TABLE "ride" (
                    ride_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    destination VARCHAR(255),
                    departure_date VARCHAR(50) NOT NULL,
                    departure_time VARCHAR(50) NOT NULL,
                    number_of_passengers INTEGER NOT NULL,
                    FOREIGN KEY (user_id)
                    REFERENCES "user" (user_id)
                )
            """,
            """
            CREATE TABLE "request" (
                    request_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    ride_id INTEGER NOT NULL,
                    request_status VARCHAR(50) NOT NULL DEFAULT 'pending',
                    FOREIGN KEY (user_id)
                        REFERENCES "user" (user_id),
                    FOREIGN KEY (ride_id)
                        REFERENCES "ride" (ride_id)
                )
            """,)
        conn = None
        try:
            conn = DatabaseAccess.database_connection()
            cur = conn.cursor()
            for command in commands:
                cur.execute(command)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
