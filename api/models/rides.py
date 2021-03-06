"""
This module handles specific requsts made
on the API end points
"""
from flask import jsonify, request
from api.models.ride import Ride
from api.models.request import Request
from api.models.database_transaction import DbTransaction
from api.models.error_messages import ErrorMessage


class RidesHandler(object):
    """
    This class contains methods that handle specific
    requests made on the API end point
    Control is obtained from the RidesView class
    """

    error_message = ErrorMessage()

    def return_all_rides(self, sql_statement, data=None):
        """
        This method returns all ride offers made
        returns ride offers in a JSON format
        :return
        """
        sql = sql_statement
        requests_turple_list = []
        if  data is not None:
            requests_turple_list = DbTransaction.retrieve_all(sql, data)
        else:
            requests_turple_list = DbTransaction.retrieve_all(sql)

        request_list = []
        for request_tuple in requests_turple_list:
            request_dict = {
                "driver_name": request_tuple[0],
                "ride_id": request_tuple[1],
                "driver_id": request_tuple[2],
                "departure_location": request_tuple[3],
                "destination": request_tuple[4],
                "departure_date": request_tuple[5],
                "departure_time": request_tuple[6],
                "number_of_passengers": request_tuple[7]
            }
            request_list.append(request_dict)
        return jsonify({"message": "results retrieved successfully",
                        "rides": request_list})

    def return_single_ride(self, ride_id):
        """
        This remothod returns a single ride offer in
        a JSON format
        :param ride_id: Ride id
        :return
        """
        request_sql = """SELECT "user".first_name, ride.* FROM "ride" LEFT JOIN "user"\
         ON(ride.user_id = "user".user_id) WHERE "ride_id" = %s """
        ride_turple = DbTransaction.retrieve_one(request_sql, (ride_id, ))

        if ride_turple is not None:
            user_name = ride_turple[0]
            ride_id = ride_turple[1]
            user_id = ride_turple[2]
            departure_location = ride_turple[3]
            destination = ride_turple[4]
            departure_date = ride_turple[5]
            departure_time = ride_turple[6]
            number_of_passengers = ride_turple[7]
            return jsonify({"Status code": 200, "ride": {
                "driver_name": user_name,
                "ride_id": ride_id,
                "driver_id": user_id,
                "departure_location": departure_location,
                "destination": destination,
                "departure_date": departure_date,
                "departure_time": departure_time,
                "number_of_passengers": number_of_passengers
            },
                            "message": "result retrieved successfully"})
        return self.error_message.no_ride_available(ride_id)

    def post_ride_offer(self, user_id):
        """
        This method saves a ride offer when a ride_id is not set
        It takes control from the post() method
        :return
        """
        keys = ("departure_location", "destination", "departure_date",
                "departure_time", "number_of_passengers")
        if not set(keys).issubset(set(request.json)):
            return self.error_message.request_missing_fields()

        request_condition = [
            request.json["departure_location"].strip(),
            request.json["destination"].strip(),
            request.json["departure_date"].strip(),
            request.json["departure_time"].strip(),
            request.json["number_of_passengers"]
            ]

        if not all(request_condition):
            return self.error_message.fields_missing_information(request.json)

        user = DbTransaction.retrieve_one(
            """SELECT "user_id" FROM "user" WHERE "user_id" = %s""",
            (user_id, ))
        if user is None:
            return self.error_message.no_user_found_response("Ride not created", request.json["ride_id"])
        departure_location = request.json['departure_location']
        destination = request.json['destination']
        departure_date = request.json['departure_date']
        departure_time = request.json['departure_time']
        number_of_passengers = request.json['number_of_passengers']

        ride = Ride(user, departure_location, destination,
                    departure_date, departure_time, number_of_passengers
                )
        ride_existance = ride.check_ride_existance()
        if ride_existance["status"] == "failure":
            return jsonify({"message": ride_existance["message"]}), 400

        ride.save_ride_offer()
        return jsonify({"status_code": 201, "ride": ride.get_ride_information(),
                        "message": "Ride added successfully"}), 201

    def post_request_to_ride_offer(self, user_id, ride_id):
        """
        This method saves a request to a ride offer when a ride_id is set
        It takes control from the post() method
        :return
        """
        db_user_id = DbTransaction.retrieve_one(
            """SELECT "user_id" FROM "user" WHERE "user_id" = %s""",
            (user_id, ))
        db_ride_id = DbTransaction.retrieve_one(
            """SELECT "ride_id" FROM "ride" WHERE "ride_id" = %s""",
            (ride_id, ))

        if db_user_id is None:
            return self.error_message.no_user_found_response("Request not made", ride_id)
        if db_ride_id is None:
            return self.error_message.no_ride_available(ride_id)

        ride_request = Request(user_id, ride_id)

        check_request = ride_request.check_request_existance()
        if check_request["status"] == "failure":
            return jsonify({"message": check_request["message"]}), 400
        
        ride_request.save_request()

        return jsonify({"Status code": 201, 
                       "request": ride_request.return_request_information(),
                        "message": "request sent successfully"}), 201
