"""
This module handles specific requsts made
on the API end points
"""
from flask import jsonify, request
from api.models.ride import Ride
from api.models.request import Request
from api.models.database_transaction import DbTransaction


class RidesHandler(object):
    """
    This class contains methods that handle specific
    requests made on the API end point
    Control is obtained from the RidesView class
    """

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
        return self.no_ride_available(ride_id)

    def post_ride_offer(self, user_id):
        """
        This method saves a ride offer when a ride_id is not set
        It takes control from the post() method
        :return
        """
        keys = ("departure_location", "destination", "departure_date",
                "departure_time", "number_of_passengers")
        if not set(keys).issubset(set(request.json)):
            return self.request_missing_fields()

        request_condition = [
            request.json["departure_location"].strip(),
            request.json["destination"].strip(),
            request.json["departure_date"].strip(),
            request.json["departure_time"].strip(),
            request.json["number_of_passengers"]
            ]

        if not all(request_condition):
            return self.fields_missing_info()
        user = DbTransaction.retrieve_one(
            """SELECT "user_id" FROM "user" WHERE "user_id" = %s""",
            (user_id, ))
        if user is None:
            return self.no_user_found_response("Ride not created", request.json["ride_id"])
        departure_location = request.json['departure_location']
        destination = request.json['destination']
        departure_date = request.json['departure_date']
        departure_time = request.json['departure_time']
        number_of_passengers = request.json['number_of_passengers']
        ride_existance = self.check_ride_existance(user, departure_location, destination,
                                                   departure_date, departure_time, number_of_passengers)
        if ride_existance["status"] == "failure":
            return jsonify({"message": ride_existance["message"]}), 400
        ride = Ride(
            user,
            departure_location,
            destination,
            departure_date,
            departure_time,
            number_of_passengers
            )

        ride_sql = """INSERT INTO "ride"(user_id, departure_location, destination,
                 departure_date, departure_time,
                 number_of_passengers)
                VALUES((%s), %s, %s, %s, %s, %s);"""
        db_user_id = DbTransaction.retrieve_one(
            """SELECT "user_id" FROM "user" WHERE "user_id" = %s""",
            (ride.user_id, ))
        ride_data = (
            db_user_id, ride.departure_location,
            ride.destination, ride.departure_date,
            ride.departure_time, ride.number_of_passengers
            )
        DbTransaction.save(ride_sql, ride_data)
        return jsonify({"status_code": 201, "ride": {
            "departure_location": ride.departure_location,
            "destination": ride.destination,
            "departure_date": ride.departure_date,
            "departure_time": ride.departure_time,
            "number_of_passengers": ride.number_of_passengers
        },
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
            return self.no_user_found_response("Request not made", ride_id)
        if db_ride_id is None:
            return self.no_ride_available(ride_id)

        check_request = self.check_request_existance(user_id, ride_id)
        if check_request["status"] == "failure":
            return jsonify({"message": check_request["message"]}), 400
        ride_request = Request(user_id, ride_id)
        ride_sql = """INSERT INTO "request"(user_id, ride_id)
            VALUES((%s), (%s));"""
        request_data = (user_id, ride_id)
        DbTransaction.save(ride_sql, request_data)
        return jsonify({"Status code": 201, "request": {
            "user_id": ride_request.user_id,
            "ride_id": ride_request.ride_id
        },
                        "message": "request sent successfully"}), 201

    @staticmethod
    def fields_missing_info():
        """
        This method returns a JSON response when some fields in
        the data sent are missing
        :return
        """
        return jsonify({"status": "failure",
                        "status_code": 400, "data": request.json,
                        "error_message": "Some fields are empty"}), 400
    @staticmethod
    def request_missing_fields():
        """
        This method returns a JSON response when containg the
        error message that some fields are missing
        :return
        """
        return jsonify({"status": "failure",
                        "error_message": "some of these fields are missing"}), 400

    @staticmethod
    def no_ride_available(ride_id):
        """
        This method returns a JSON response with a message of no ride
        found
        :return
        """
        return jsonify({"status": "failure",
                        "message": "No ride available with id: " + str(ride_id)}), 200

    @staticmethod
    def no_user_found_response(message, user_id):
        """
        This method returns an error message when a user
        of a specific id is not found
        :return:
        """
        return jsonify({"status": "failure",
                        "message": message,
                        "error_message": "No user found with id: " + str(user_id)
                       }), 400
    @staticmethod
    def check_ride_existance(user_id, departure_location, destination,
                             departure_date, departure_time, number_of_passengers):
        """
        This method checks if a ride exists already.
        If a ride does not not exists, it returns a success message else
        it returns a failure message
        """
        sql = """SELECT "user_id", "destination", "departure_date", "departure_time",
        "number_of_passengers" FROM "ride" WHERE "user_id" = %s
        AND "departure_location" = %s AND "destination" = %s 
        AND "departure_date" = %s AND "departure_time" = %s AND "number_of_passengers" = %s"""
        ride_data = (user_id, departure_location, destination, departure_date,
                     departure_time, number_of_passengers)
        ride = DbTransaction.retrieve_one(sql, ride_data)
        if ride is None:
            return {"status": "success", "message": "Ride does not exists"}
        return {"status": "failure", "message": "Ride already exists"}

    @staticmethod
    def check_request_existance(user_id, ride_id):
        """
        Checks the existance of a request made by a user.
        I a request exists, it returns a failure message that the request already exists
        otherwise, a success message is returned showing that a request does not exist.
        """
        check_sql = """SELECT "user_id", "ride_id" FROM "request"
        WHERE "user_id" = %s AND "ride_id" = %s"""
        request_data = (user_id, ride_id)
        ride_request = DbTransaction.retrieve_one(check_sql, request_data)
        if ride_request is None:
            return {"status": "success", "message": "Request does not exists"}
        return {"status": "failure", "message": "Request already exists"}
