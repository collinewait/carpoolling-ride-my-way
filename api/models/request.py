"""
This module is a request model with its attributes
"""


class Request(object):
    """
    This class represents a Request entity
    """

    def __init__(self, user_id, ride_id, request_id=None):
        self.user_id = user_id
        self.ride_id = ride_id
        self.request_id = request_id
        