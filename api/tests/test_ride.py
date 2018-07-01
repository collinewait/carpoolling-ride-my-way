"""
This module contains tests for the api end points.
"""
from unittest import TestCase
from datetime import datetime
from flask import json
from api import APP
from api.models.user import User
from api.models.ride import Ride
from api.models.request import Request


class TestRideTestCase(TestCase):
    """
    Tests run for the api end pints.
    """

    date_time = datetime.now()
    depart_date = date_time.strftime("%x")
    depart_time = date_time.strftime("%H:%M")

    user_test = User(123, "Jack", "Ma", "jack@ma.com", "0771462657", "1234")
    user1 = User(1234, "Colline", "Wait", "coll@wait.com", "0771462657", "1234")
    user2 = User(1235, "Vicky", "Von", "vic@vom.com", "0771658399", "1234")

    ride1 = Ride(
        1, user1.first_name, user1.last_name,
        "Ntinda", depart_date, depart_time, 2
    )
    ride2 = Ride(
        2, user2.first_name, user2.last_name,
        "Mukon", depart_date, depart_time, 4
    )

    request = Request(1, 1, user1.first_name, user1.user_id, user1.phone_number)

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = APP
        self.client = self.app.test_client
        self.client().post('/api/v1/rides/', data=json.dumps(
            self.ride1.__dict__), content_type='application/json')
        self.client().post('/api/v1/rides/', data=json.dumps(
            self.ride2.__dict__), content_type='application/json')


    def test_api_gets_all_ride_offers(self):
        """
        Test API can get all ride offers (GET request).
        """
        response = self.client().get('/api/v1/rides/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json['rides'], list)
        self.assertTrue(response.json["rides"])
        self.assertIsInstance(response.json["rides"][0], dict)
        self.assertIn(1, response.json["rides"][0].values())
        self.assertIn(2, response.json["rides"][1].values())
        self.assertIn("results retrieved successfully", response.json["message"])

    def test_get_one_ride_offer(self):
        """
        Test an item (a ride) is returned on a get request.
        (GET request)
        """
        response = self.client().get('/api/v1/rides/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("ride", response.json)
        self.assertIn("result retrieved successfully", response.json["message"])
        self.assertIsInstance(response.json['ride'], dict)
        self.assertEqual(len(response.json['ride']), 7)

    def test_ride_attributes_returned(self):
        """
        Test that all values expected  in a ride dictionary are returned
        """
        response = self.client().get('/api/v1/rides/1')
        self.assertIn(1, response.json['ride'].values())
        self.assertIn("Colline", response.json['ride']["driver_firstname"])
        self.assertIn("Wait", response.json['ride']["driver_lastname"])
        self.assertIn("Ntinda", response.json['ride']["destination"])
        self.assertEqual(2, response.json['ride']["number_of_passengers"])
        self.assertEqual(self.depart_date, response.json['ride']["departure_date"])
        self.assertEqual(self.depart_time, response.json['ride']["departure_time"])

    def test_ride_not_found(self):
        """
        Test API returns nothing when a ride is not found
        A return contsins a status code of 200
        """
        response = self.client().get('/api/v1/rides/20')
        self.assertEqual(response.status_code, 200)
        self.assertEqual("No ride available with id: 20", response.json['message'])

    def test_error_hander_returns_json(self):
        """
        Test API returns a json format response when the user hits
        a wrong api end point
        """
        response = self.client().get('/api/v1/rides/me')
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response.json, dict)
        self.assertEqual("The requested resource was not found on the server",
                         response.json["error_message"])
        self.assertEqual(404, response.json["status_code"])
        self.assertEqual("http://localhost/api/v1/rides/me",
                         response.json["url"])

    def test_post_creates_a_ride_offer(self):
        """
        This method tests for the creation of a ride offer
        (POST request)
        """
        response = self.client().post('/api/v1/rides/', data=json.dumps(
            self.ride1.__dict__), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn("ride", response.json)
        self.assertIn("message", response.json)
        self.assertEqual("Ride added successfully", response.json['message'])
        self.assertTrue(response.json['ride'])

    def test_non_json_data_not_sent(self):
        """
        This method tests that non json data is not sent
        """
        response = self.client().post('/api/v1/rides/', data=json.dumps(
            self.ride1.__dict__), content_type='text/plain')

        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json)
        self.assertEqual("content not JSON", response.json['error_message'])

    def test_empty_attributes_not_sent(self):
        """
        This method tests that data is not sent with empty fields
        """
        response = self.client().post('/api/v1/rides/', data=json.dumps(
            dict(driver_firstname=self.user1.first_name,
                 driver_lastname=self.user1.last_name, destination="Mbarara",
                 departure_date="", departure_time="",
                 number_of_passengers=2)), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json)
        self.assertEqual("Some fields are empty", response.json['error_message'])

    def test_partial_fields_not_sent(self):
        """
        This method tests that data with partial fields is not send
        on creating a ride offer
        """
        response = self.client().post('/api/v1/rides/', data=json.dumps(
            dict(driver_firstname=self.user1.first_name,
                 driver_lastname=self.user1.last_name, destination="Mbarara",
                 number_of_passengers=2)), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual("some of these fields are missing",
                         response.json['error_message'])

    def test_post_joins_a_ride_offer(self):
        """
        This method tests the joinig of a ride offer
        (POST request)
        """

        response = self.client().post('/api/v1/rides/1/requests', data=json.dumps(
            self.request.__dict__), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn("request", response.json)
        self.assertEqual("request sent successfully", response.json['message'])
        self.assertTrue(response.json['request'])

    def test_non_json_request_not_sent(self):
        """
        This method tests that non json request is not sent
        """
        response = self.client().post('/api/v1/rides/1/requests', data=json.dumps(
            self.request.__dict__), content_type='text/plain')
        self.assertEqual(response.status_code, 400)
        self.assertEqual("content not JSON", response.json['error_message'])

    def test_empty_request_attributes(self):
        """
        This method tests that data is not sent with empty fields
        """
        response = self.client().post('/api/v1/rides/1/requests', data=json.dumps(
            dict(passenger_name="", passenger_id=self.user_test.user_id,
                 passenger_contact=self.user_test.phone_number
                )), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json)
        self.assertEqual("Some fields are empty", response.json['error_message'])

    def test_non_existing_ride_request(self):
        """
        This method tests that a request made to a non existing
        ride offer returns a JSON response showing ride not
        found
        """
        response = self.client().post('/api/v1/rides/22/requests', data=json.dumps(
            self.request.__dict__), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual("No ride available with id: 22", response.json['message'])

    def test_partial_request_sent(self):
        """
        This method tests that data with partial fields is not send
        on creating a ride offer
        """
        response = self.client().post('/api/v1/rides/1/requests', data=json.dumps(
            dict(passenger_contact=self.user_test.phone_number)),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual("some of these fields are missing",
                         response.json['error_message'])
