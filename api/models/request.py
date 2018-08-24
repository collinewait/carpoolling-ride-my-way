"""
This module is a request model with its attributes
"""
from api.models.database_transaction import DbTransaction


class Request(object):
    """
    This class represents a Request entity
    """

    def __init__(self, user_id, ride_id, request_id=None):
        self.user_id = user_id
        self.ride_id = ride_id
        self.request_id = request_id

    def save_request(self):
        """
        This method saves a request made to a ride offer.
        """

        request_sql = """INSERT INTO "request"(user_id, ride_id)
            VALUES((%s), (%s));"""
        request_data = (self.user_id, self.ride_id)
        DbTransaction.save(request_sql, request_data)
        
    def return_request_information(self):
        """
        This method returns the information of a class.
        """
        
        return {
            "user_id": self.user_id,
            "ride_id": self.ride_id
        }

    def check_request_existance(self):
        """
        Checks the existance of a request made by a user.
        I a request exists, it returns a failure message that the request already exists
        otherwise, a success message is returned showing that a request does not exist.
        """
        check_sql = """SELECT "user_id", "ride_id" FROM "request"
        WHERE "user_id" = %s AND "ride_id" = %s"""
        request_data = (self.user_id, self.ride_id)
        ride_request = DbTransaction.retrieve_one(check_sql, request_data)
        if ride_request is None:
            return {"status": "success", "message": "Request does not exists"}
        return {"status": "failure", "message": "Request already exists"}
