"""
This module provides responses to url requests.
"""
from flask import jsonify, request
from flask.views import MethodView
from api.models.rides import RidesHandler


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
        if not ride_id:
            return self.rides_handler.return_all_rides()

        return self.rides_handler.return_single_ride(ride_id)

    def post(self, ride_id):
        """"
        Handles post requests
        saves a ride offer if ride_id is not set
        and saves a request to a ride if ride_id is set
        :return:
        """
        if not request or not request.json:
            return jsonify({"status_code": 400, "data": str(request.data),
                            "error_message": "content not JSON"}), 400

        if ride_id:

            return self.rides_handler.post_request_to_ride_offer(ride_id)

        return self.rides_handler.post_ride_offer()
