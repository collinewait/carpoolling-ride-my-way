"""
This module provides responses to url requests.
"""
from flask import jsonify, request
from flask.views import MethodView
from api.models.rides import RidesHandler
from api.models.requests import RequestModel
from api.models.user import User


class RideViews(MethodView):
    """
    This class contains methods that respond to various url end points.
    """

    rides_handler = RidesHandler()

    user_obj = User()

    def get(self, ride_id):
        """
        All ride offers are returned when no ride_id is specified at the end point
        if a ride id is not set, return_all_rides() method is called
        and if a ride id is set, return_single_ride(ride_id) method is called
        :param ride_id: Ride id
        :return:
        """
        token = request.headers.get('auth_token')
        if not token:
            return jsonify({"message": "Token is missing"}), 401

        decoded = self.user_obj.decode_token(request.headers.get('auth_token'))
        if decoded["state"] == "Failure":
            return User.decode_failure(decoded["error_message"])

        if User.check_login_status(decoded["user_id"]):
            if not ride_id:
                request_sql = """SELECT "user".first_name, ride.* FROM "ride" LEFT JOIN "user"\
                ON(ride.user_id = "user".user_id) WHERE "ride".user_id != %s"""
                sql_data = (decoded["user_id"], )
                return self.rides_handler.return_all_rides(request_sql, sql_data)
            return self.rides_handler.return_single_ride(ride_id)
        return jsonify({"message": "Please login"}), 401

    def post(self, ride_id):
        """"
        Handles post requests
        saves a ride offer if ride_id is not set
        and saves a request to a ride if ride_id is set
        :return:
        """
        token = request.headers.get('auth_token')
        if not token:
            return jsonify({"message": "Token is missing"}), 401

        decoded = self.user_obj.decode_token(request.headers.get('auth_token'))
        if decoded["state"] == "Failure":
            return User.decode_failure(decoded["error_message"])
        if User.check_login_status(decoded["user_id"]):
            if ride_id:
                return self.rides_handler.post_request_to_ride_offer(decoded["user_id"], ride_id)
            if not request or not request.json:
                return jsonify({"status_code": 400, "data": str(request.data),
                                "error_message": "content not JSON"}), 400
            return self.rides_handler.post_ride_offer(decoded["user_id"])
        return jsonify({"message": "Please login"}), 401


class RequestView(MethodView):
    """
    This class handles url endpoints for requests.
    """
    request_model = RequestModel()

    user_obj = User()

    def get(self, ride_id):
        """
        This method gets all requests made on a ride offer
        """
        token = request.headers.get('auth_token')
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        decoded = self.user_obj.decode_token(request.headers.get('auth_token'))
        if decoded["state"] == "Failure":
            return User.decode_failure(decoded["error_message"])
        if User.check_login_status(decoded["user_id"]):
            return self.request_model.return_all_requests(ride_id)
        return jsonify({"message": "Please login"}), 401

    def put(self, ride_id, request_id):
        """
        This method Edits a request with a valid Id. The request content-type must be json
        It delegates the work to edit_request(ride_id, request_id) method
        :param ride_id: Ride Id
        :param request_id: Request Id
        :return: Response of Edited request.
        """
        token = request.headers.get('auth_token')
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        decoded = self.user_obj.decode_token(request.headers.get('auth_token'))
        if decoded["state"] == "Failure":
            return User.decode_failure(decoded["error_message"])
        if User.check_login_status(decoded["user_id"]):
            return self.request_model.edit_request(ride_id, request_id)
        return jsonify({"message": "Please login"}), 401


class RequestsTaken(MethodView):
    """
    This class handles requests made by a specific user
    by joining a ride
    """
    request = RequestModel()
    user_obj = User()

    def get(self):
        """
        This method gets all requests made on a specific user
        """
        token = request.headers.get('auth_token')
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        decoded = self.user_obj.decode_token(request.headers.get('auth_token'))
        if decoded["state"] == "Failure":
            return User.decode_failure(decoded["error_message"])
        if User.check_login_status(decoded["user_id"]):
            return self.request.return_all_requests(decoded["user_id"])
        return jsonify({"message": "Please login"}), 401


class RidesGiven(MethodView):
    """
    This class handles rides made by a user
    """
    rides = RidesHandler()
    request = RequestModel()
    user_obj = User()
    
    def get(self):
        """
        This method gets all ride offers made by a specific user
        """
        token = request.headers.get('auth_token')
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        decoded = self.user_obj.decode_token(request.headers.get('auth_token'))
        if decoded["state"] == "Failure":
            return User.decode_failure(decoded["error_message"])
        if User.check_login_status(decoded["user_id"]):
            ride_sql = """SELECT "user".first_name, ride.* FROM "ride" LEFT JOIN "user"\
            ON(ride.user_id = "user".user_id) WHERE "ride".user_id = %s """
            sql_data = (decoded["user_id"], )
            return self.rides.return_all_rides(ride_sql, sql_data)
        return jsonify({"message": "Please login"}), 401
