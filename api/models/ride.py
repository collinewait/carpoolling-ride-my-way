"""
This module is a ride model with its attributes
"""
from api.models.database_transaction import DbTransaction


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

    def save_ride_offer(self):
        """
        This method persists the ride offer
        """

        ride_sql = """INSERT INTO "ride"(user_id, departure_location, destination,
            departure_date, departure_time,
            number_of_passengers)
        VALUES((%s), %s, %s, %s, %s, %s);"""
        ride_data = (
            self.user_id, self.departure_location,
            self.destination, self.departure_date,
            self.departure_time, self.number_of_passengers
            )
        DbTransaction.save(ride_sql, ride_data)
