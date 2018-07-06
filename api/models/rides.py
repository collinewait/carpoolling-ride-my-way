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

    rides = []

    requests = []

    def return_all_rides(self):
        """
        This method returns all ride offers made
        returns ride offers in a JSON format
        :return
        """
        request_sql = """SELECT "user".first_name, ride.* FROM "ride" LEFT JOIN "user" ON(ride.user_id = "user".user_id)"""
        requests_turple_list = DbTransaction.retrieve_all(request_sql)
        request_list = []
        for request_tuple in requests_turple_list:
            request_dict = {
                "driver_name": request_tuple[0],
                "ride_id": request_tuple[1],
                "driver_id": request_tuple[2],
                "destination": request_tuple[3],
                "departure_date": request_tuple[4],
                "departure_time": request_tuple[5],
                "number_of_passengers": request_tuple[6]
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
        request_sql = """SELECT "user".first_name, ride.* FROM "ride" LEFT JOIN "user" ON(ride.user_id = "user".user_id) WHERE "ride_id" = %s """
        ride_turple = DbTransaction.retrieve_one(request_sql, (ride_id, ))

        if ride_turple is not None:
            ride = {
                "driver_name": ride_turple[0],
                "ride_id": ride_turple[1],
                "driver_id": ride_turple[2],
                "destination": ride_turple[3],
                "departure_date": ride_turple[4],
                "departure_time": ride_turple[5],
                "number_of_passengers": ride_turple[6]
            }
            return jsonify({"Status code": 200, "ride": ride,
                            "message": "result retrieved successfully"})
        return self.no_ride_available(ride_id)

    def post_ride_offer(self):
        """
        This method saves a ride offer when a ride_id is not set
        It takes control from the post() method
        :return
        """
        keys = ("user_id", "destination", "departure_date",
                "departure_time", "number_of_passengers")
        if not set(keys).issubset(set(request.json)):
            return self.request_missing_fields()

        request_condition = [
            request.json["user_id"], request.json["destination"],
            request.json["departure_date"], request.json["departure_time"],
            request.json["number_of_passengers"]
            ]

        if not all(request_condition):
            return self.fields_missing_info()
        user = DbTransaction.retrieve_one(
            """SELECT "user_id" FROM "user" WHERE "user_id" = %s""",
            (request.json["user_id"], ))
        if user is None:
            return jsonify({"status": "Request not made",
                            "message": "No user found with id: " + str(request.json["user_id"])
                           }), 401
        ride = Ride(
            request.json['user_id'],
            request.json['destination'],
            request.json['departure_date'],
            request.json['departure_time'],
            request.json['number_of_passengers'],
            len(self.rides) + 1
            )

        ride_sql = """INSERT INTO "ride"(user_id, destination, departure_date, departure_time,
                 number_of_passengers)
                VALUES((%s), %s, %s, %s, %s);"""
        db_user_id = DbTransaction.retrieve_one(
            """SELECT "user_id" FROM "user" WHERE "user_id" = %s""",
            (ride.user_id, ))
        ride_data = (
            db_user_id,
            ride.destination, ride.departure_date,
            ride.departure_time, ride.number_of_passengers
            )
        DbTransaction.save(ride_sql, ride_data)
        self.rides.append(ride)
        return jsonify({"status_code": 201, "ride": ride.__dict__,
                        "message": "Ride added successfully"}), 201

    def post_request_to_ride_offer(self, ride_id):
        """
        This method saves a request to a ride offer when a ride_id is set
        It takes control from the post() method
        :return
        """
        request_keys = ("user_id", "ride_id")
        if not set(request_keys).issubset(set(request.json)):
            return self.request_missing_fields()

        ride_request = [
            request.json["user_id"],
            request.json["ride_id"]
        ]

        if not all(ride_request):
            return self.fields_missing_info()
        user = DbTransaction.retrieve_one(
            """SELECT "user_id" FROM "user" WHERE "user_id" = %s""",
            (request.json["user_id"], ))
        if user is None:
            return jsonify({"status": "Request not made",
                "message": "No user found with id: " + str(request.json["user_id"])
                }), 401
        for ride in self.rides:
            if ride.ride_id == ride_id:
                ride_request = Request(
                    request.json["user_id"],
                    request.json["ride_id"],
                    len(self.requests) + 1
                )
                ride_sql = """INSERT INTO "request"(user_id, ride_id)
                    VALUES((%s), (%s));"""
                db_user_id = DbTransaction.retrieve_one(
                    """SELECT "user_id" FROM "user" WHERE "user_id" = %s""",
                    (ride_request.user_id, ))
                db_ride_id = DbTransaction.retrieve_one(
                    """SELECT "ride_id" FROM "ride" WHERE "ride_id" = %s""",
                    (ride_request.ride_id, ))
                request_data = (db_user_id, db_ride_id)
                DbTransaction.save(ride_sql, request_data)
                self.requests.append(ride_request.__dict__)
                return jsonify({"Status code": 201, "request": ride_request.__dict__,
                                "message": "request sent successfully"}), 201

        return self.no_ride_available(ride_id)

    @staticmethod
    def fields_missing_info():
        """
        This method returns a JSON response when some fields in
        the data sent are missing
        :return
        """
        return jsonify({"status_code": 400, "data": request.json,
                        "error_message": "Some fields are empty"}), 400
    @staticmethod
    def request_missing_fields():
        """
        This method returns a JSON response when containg the
        error message that some fields are missing
        :return
        """
        return jsonify({"error_message": "some of these fields are missing"}), 400

    @staticmethod
    def no_ride_available(ride_id):
        """
        This method returns a JSON response with a message of no ride
        found
        :return
        """
        return jsonify({"message": "No ride available with id: " + str(ride_id)}), 200
