"""
This module is respomsible for request end points.
"""
from flask import jsonify
from api.models.database_transaction import DbTransaction
from api.models.rides import RidesHandler


class RequestModel(object):
    """
    This class contains methods that handle specific
    requests made on the API end point in regard to requests
    made on rides
    """

    def return_all_requests(self, ride_id):
        """
        This method returns all requests made on a ride offer made
        returns ride offers in a JSON format
        :return
        """
        confirm_ride_id = DbTransaction.retrieve_one(
            """SELECT "ride_id" FROM "ride" WHERE "ride_id" = %s""",
            (ride_id, ))

        if confirm_ride_id:
            request_sql = """SELECT "user".first_name, request.* FROM "request" LEFT JOIN "user" ON(request.user_id = "user".user_id) WHERE "ride_id" = %s"""
            requests_turple_list = DbTransaction.retrieve_all(request_sql, (ride_id,))
            request_list = []
            for request_tuple in requests_turple_list:
                request_dict = {
                    "first_name": request_tuple[0],
                    "request_id": request_tuple[1],
                    "user_id": request_tuple[2],
                    "ride_id": request_tuple[3]
                }
                request_list.append(request_dict)

            return jsonify({"message": "result retrieved successfully",
                            "requests": request_list}), 200
        return RidesHandler.no_ride_available(ride_id)
