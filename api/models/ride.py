"""
This module is a ride model with its attributes
"""


class Ride(object):
    """
    This class represents a Ride entity
    """

    def __init__(self, *args):
        self.user_id = args[0]
        self.departure_location = args[1]
        self.destination = args[2]
        self.departure_date = args[3]
        self.departure_time = args[4]
        self.number_of_passengers = args[5]
        if len(args) > 6:
            self.ride_id = args[6]
        else:
            self.ride_id = None
