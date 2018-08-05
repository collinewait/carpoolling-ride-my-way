"""
This module is respomsible for request end points.
"""
from flask import jsonify, request
from api.models.database_transaction import DbTransaction
from api.models.rides import RidesHandler


class RequestModel(object):
    """
    This class contains methods that handle specific
    requests made on the API end point in regard to requests
    made on rides
    """

    sql = """ SELECT "user".first_name as passenger,
            "ride".user_id as driver_id, t1.first_name as driver_name,
            request.* FROM request JOIN "user" ON("request".user_id = "user".user_id)\
            JOIN "ride" ON("request".ride_id = "ride".ride_id) JOIN "user" t1\
            ON(t1.user_id = "ride".user_id)"""

    def return_all_requests(self, ride_id=None, user_id=None):
        """
        This method returns all requests made on a ride offer made
        returns ride offers in a JSON format
        :return
        """
        confirm_id = None
        request_sql = None
        request_data = None

        if user_id:
            confirm_id = DbTransaction.retrieve_one(
                """SELECT "user_id" FROM "user" WHERE "user_id" = %s""",
                (user_id, ))
            request_sql = request_sql = self.sql + """ WHERE "request".user_id = %s"""
            request_data = (user_id, )
        else:
            confirm_id = DbTransaction.retrieve_one(
                """SELECT "ride_id" FROM "ride" WHERE "ride_id" = %s""",
                (ride_id, ))
            request_sql = self.sql + """ WHERE "request".ride_id = %s"""
            request_data = (ride_id, )

        if confirm_id:
            requests_turple_list = DbTransaction.retrieve_all(request_sql, request_data)
            request_list = []
            for request_tuple in requests_turple_list:
                request_dict = {
                    "passenger_name": request_tuple[0],
                    "driver_id": request_tuple[1],
                    "driver_name": request_tuple[2],
                    "request_id": request_tuple[3],
                    "user_id": request_tuple[4],
                    "ride_id": request_tuple[5],
                    "request_status": request_tuple[6]
                }
                request_list.append(request_dict)

            return jsonify({"message": "result retrieved successfully",
                            "requests": request_list}), 200
        if user_id:
            RidesHandler.no_user_found_response("No requests found", user_id)
        return RidesHandler.no_ride_available(ride_id)

    def edit_request(self, ride_id, request_id):
        """
        This method edits a request made to a ride
        It get control from an PUT method in view
        """
        if request.content_type == 'application/json':
            db_ride_id = DbTransaction.retrieve_one(
                """SELECT "ride_id" FROM "ride" WHERE "ride_id" = %s""",
                (ride_id, ))
            db_request_id = DbTransaction.retrieve_one(
                """SELECT "request_id" FROM "request" WHERE "request_id" = %s""",
                (request_id, ))

            if db_ride_id:
                if db_request_id:
                    edit_sql = """UPDATE request SET request_status = %s
                    WHERE request_id = %s"""
                    edit_data = (request.json["request_status"], request_id)
                    nummber_of_updated_rows = DbTransaction.edit(edit_sql, edit_data)
                    return jsonify({"status": "success",
                                    "message": "request " + request.json["request_status"] + " successfully.\
                                    " + str(nummber_of_updated_rows) + " row(s) updated"}), 200
                return self.no_request_found(request_id)
            return RidesHandler.no_ride_available(ride_id)
        return jsonify({"Staus": "failure", "message": "Content-type must be JSON"}), 400

    @staticmethod
    def no_request_found(request_id):
        """
        Returns a message of no vailable request of a specific id
        No request available with id: #
        :return
        """
        return jsonify({"status": "failure",
                        "message": "No request available with id: " + str(request_id)}), 200
