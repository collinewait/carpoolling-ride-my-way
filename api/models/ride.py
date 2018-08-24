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

    def get_ride_information(self):
        """
        This method returns the information of a ride.
        """

        return {
            "departure_location": self.departure_location,
            "destination": self.destination,
            "departure_date": self.departure_date,
            "departure_time": self.departure_time,
            "number_of_passengers": self.number_of_passengers
        }

    def check_ride_existance(self):
        """
        This method checks if a ride exists already.
        If a ride does not not exists, it returns a success message else
        it returns a failure message
        """
        sql = """SELECT "user_id", "destination", "departure_date", "departure_time",
        "number_of_passengers" FROM "ride" WHERE "user_id" = %s
        AND "departure_location" = %s AND "destination" = %s 
        AND "departure_date" = %s AND "departure_time" = %s AND "number_of_passengers" = %s"""
        ride_data = (self.user_id, self.departure_location, self.destination, self.departure_date,
                    self.departure_time, self.number_of_passengers)
        ride = DbTransaction.retrieve_one(sql, ride_data)
        if ride is None:
            return {"status": "success", "message": "Ride does not exists"}
        return {"status": "failure", "message": "Ride already exists"}