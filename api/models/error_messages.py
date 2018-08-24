"""
This module returns meaningful error messages.
"""
from flask import jsonify


class ErrorMessage(object):
    """
    This class contains methods to that return error messages.
    """

    def fields_missing_information(self, request_data):
        """
        This method returns a JSON response when some fields in
        the data sent are missing
        :return
        """
        return jsonify({"status": "failure",
                        "status_code": 400, "data": request_data,
                        "error_message": "Some fields are empty"}), 400

    def request_missing_fields(self):
        """
        This method returns a JSON response when containg the
        error message that some fields are missing
        :return
        """
        return jsonify({"status": "failure",
                        "error_message": "some of these fields are missing"}), 400

    def no_ride_available(self, ride_id):
        """
        This method returns a JSON response with a message of no ride
        found
        :return
        """
        return jsonify({"status": "failure",
                        "message": "No ride available with id: " + str(ride_id)}), 200

    def no_user_found_response(self, message, user_id):
        """
        This method returns an error message when a user
        of a specific id is not found
        :return:
        """
        return jsonify({"status": "failure",
                        "message": message,
                        "error_message": "No user found with id: " + str(user_id)
                       }), 400

    def no_request_found(self, request_id):
        """
        Returns a message of no vailable request of a specific id
        No request available with id: #
        :return
        """
        return jsonify({"status": "failure",
                        "message": "No request available with id: " + str(request_id)}), 200