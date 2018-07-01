"""
This module is a request model with its attributes
"""


class Request(object):
    """
    This class represents a Request entity
    """

    def __init__(self, *args):
        self.request_id = args[0]
        self.ride_id = args[1]
        self.passenger_name = args[2]
        self.passenger_id = args[3]
        self.passenger_contact = args[4]
        