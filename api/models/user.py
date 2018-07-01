"""
This module is a ride model with its attributes
"""
class User(object):
    """
    This class represents a User entity
    """
    def __init__(self, *args):
        self.user_id = args[0]
        self.first_name = args[1]
        self.last_name = args[2]
        self.email_address = args[3]
        self.phone_number = args[4]
        self.password = args[5]
