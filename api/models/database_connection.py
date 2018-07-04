"""
This module handles the database set up
"""
import psycopg2

class DatabaseAccess(object):
    """
    This class contains methods to create a database connection
    and database table creation
    """
    APP = None

    @classmethod
    def database_connection(cls):
        """
        This method creates a connection to the databse
        "dbname='testdb' user='test123' host='localhost' password='test123' port='5432'"
        :retun: connection
        """
        app = cls.APP
        if not app.config['TESTING']:
            connection = psycopg2.connect(
                "dbname='carpooldb' user='carpooldb12' host='localhost' password='carpooldb12' port='5432'"
            )
            print("connected to the database")
            return connection
        connection = psycopg2.connect(
            "dbname='testdb' user='test123' host='localhost' password='test123' port='5432'"
        )
        print("connected to the test database")
        return connection

    @classmethod
    def create_tables(cls, app):
        """
        This method creates tables in the PostgreSQL database.
        It conects to the databse and creates tables one by one
        for command in commands:
                cur.execute(command)
        """
        cls.APP = app
        commands = (
            """
            DROP TABLE IF EXISTS "user" CASCADE;
            CREATE TABLE "user" (
                    user_id SERIAL PRIMARY KEY,
                    public_id VARCHAR(50)  UNIQUE,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    email_address VARCHAR(50) UNIQUE NOT NULL,
                    phone_number INTEGER NOT NULL,
                    password VARCHAR(80) NOT NULL
                )
            """,
            """
            DROP TABLE IF EXISTS "ride" CASCADE;
            CREATE TABLE "ride" (
                    ride_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    destination VARCHAR(255)  UNIQUE,
                    departure_date VARCHAR(50) NOT NULL,
                    departure_time VARCHAR(50) NOT NULL,
                    number_of_passengers VARCHAR(50) UNIQUE NOT NULL,
                    FOREIGN KEY (user_id)
                    REFERENCES "user" (user_id)
                )
            """,
            """
            DROP TABLE IF EXISTS "request" CASCADE;
            CREATE TABLE "request" (
                    request_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    ride_id INTEGER NOT NULL,
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
            print("cursor obtained")
            for command in commands:
                cur.execute(command)
                print ("command executed")
            cur.close()
            conn.commit()
            print("command committed")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
