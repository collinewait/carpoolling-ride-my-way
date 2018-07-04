"""
This module is a ride model with its attributes
"""


class Ride(object):
    """
    This class represents a Ride entity
    """

    def __init__(self, *args):
        self.user_id = args[0]
        self.destination = args[1]
        self.departure_date = args[2]
        self.departure_time = args[3]
        self.number_of_passengers = args[4]
        if len(args) > 5:
            self.ride_id = args[5]
        else:
            self.ride_id = None
