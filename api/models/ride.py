"""
This module is a ride model with its attributes
"""


class Ride(object):
    """
    This class represents a Ride entity
    """

    def __init__(self, *args):
        self.ride_id = args[0]
        self.driver_firstname = args[1]
        self.driver_lastname = args[2]
        self.destination = args[3]
        self.departure_date = args[4]
        self.departure_time = args[5]
        self.number_of_passengers = args[6]
