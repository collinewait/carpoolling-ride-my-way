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

    def get(self, ride_id):
        """
        All ride offers are returned when no ride_id is specified at the end point
        if a ride id is not set, return_all_rides() method is called
        and if a ride id is set, return_single_ride(ride_id) method is called
        :param ride_id: Ride id
        :return:
        """
        try:

            token = request.headers.get('auth_token')
            if not token:
                return jsonify({"message": "Token is missing"}), 401

            decoded = User.decode_token(request.headers.get('auth_token'))
            if decoded["state"] == "Failure":
                return jsonify({"message": decoded["message"]}), 401

            if not ride_id:
                return self.rides_handler.return_all_rides()

            return self.rides_handler.return_single_ride(ride_id)
        except KeyError as k:
            return jsonify({"message": "invalid token",
                            "error_message": k}), 401

    def post(self, ride_id):
        """"
        Handles post requests
        saves a ride offer if ride_id is not set
        and saves a request to a ride if ride_id is set
        :return:
        """
        try:

            token = request.headers.get('auth_token')
            if not token:
                return jsonify({"message": "Token is missing"}), 401

            decoded = User.decode_token(request.headers.get('auth_token'))
            if decoded["state"] == "Failure":
                return jsonify({"message": decoded["message"]}), 401
            if not request or not request.json:
                return jsonify({"status_code": 400, "data": str(request.data),
                                "error_message": "content not JSON"}), 400
            if ride_id:
                return self.rides_handler.post_request_to_ride_offer(ride_id)
            return self.rides_handler.post_ride_offer()
        except KeyError as k:
            return jsonify({"message": "invalid token",
                            "error_message": k}), 401


class RequestView(MethodView):
    """
    This class handles url endpoints for requests.
    """
    request_model = RequestModel()

    def get(self, ride_id):
        """
        This class gets all requests made on a ride offer
        """
        try:
            token = request.headers.get('auth_token')
            if not token:
                return jsonify({"message": "Token is missing"}), 401
            decoded = User.decode_token(request.headers.get('auth_token'))
            if decoded["state"] == "Failure":
                return jsonify({"message": decoded["message"]}), 401
            return self.request_model.return_all_requests(ride_id)
        except KeyError as k:
            return jsonify({"message": "invalid token",
                            "error_message": k}), 401
