"""
This module contains tests for the api end points.
"""
import uuid
from unittest import TestCase
from datetime import datetime
from flask import json
import psycopg2
from api import APP
from api.models.user import User
from api.models.ride import Ride
from api.models.request import Request
from api.models.database_connection import DatabaseAccess


class TestRideTestCase(TestCase):
    """
    Tests run for the api end pints.
    """

    date_time = datetime.now()
    depart_date = date_time.strftime("%x")
    depart_time = date_time.strftime("%H:%M")

    user_test = User(123, "Jack", "Ma", "jack@ma.com", "0771462657", "1234")
    user11 = User(1234, "Colline", "Wait", "coll@wait.com", "0771462657", "1234")
    user12 = User(1235, "Vicky", "Von", "vic@vom.com", "0771658399", "1234")

    ride1 = Ride(
        1, "Ntinda", depart_date, depart_time, 2
    )
    ride2 = Ride(
        2, "Mukon", depart_date, depart_time, 4
    )

    request = Request(1, 1)
    request1 = Request(2, 1)
    request2 = Request(1, 1)

    user1 = User(str(uuid.uuid4), "coco", "wait",
                 "col@stev.com", "0772587", "123111")
    user2 = User(str(uuid.uuid4), "colline", "wait",
                 "colline@rec.com", "0772587", "12311")

    def setUp(self):
        """Define test variables and initialize app."""
        APP.config['TESTING'] = True
        self.app = APP
        self.client = self.app.test_client
        DatabaseAccess.create_tables(APP)
        self.client().post('/api/v1/auth/signup/', data=json.dumps(
            self.user1.__dict__), content_type='application/json')
        self.client().post('/api/v1/auth/signup/', data=json.dumps(
            self.user2.__dict__), content_type='application/json')
        self.client().post('/api/v1/rides/', data=json.dumps(
            self.ride1.__dict__), content_type='application/json',
                           headers=({"auth_token": self.generate_token()}))
        self.client().post('/api/v1/rides/', data=json.dumps(
            self.ride2.__dict__), content_type='application/json',
                           headers=({"auth_token": self.generate_token()}))
        self.client().post('/api/v1/rides/1/requests/', data=json.dumps(
            self.request1.__dict__), content_type='application/json',
                           headers=({"auth_token": self.generate_token()}))
        self.client().post('/api/v1/rides/1/requests/', data=json.dumps(
            self.request2.__dict__), content_type='application/json',
                           headers=({"auth_token": self.generate_token()}))

    def generate_token(self):
        """
        This method gets a token to be used for authentication when
        making requests.
        """
        response = self.client().post(
            '/api/v1/auth/login/',
            data=json.dumps(dict(
                email_address=self.user1.email_address,
                password=self.user1.password
            )),
            content_type='application/json'
        )
        return response.json["auth_token"]

    def test_api_gets_all_ride_offers(self):
        """
        Test API can get all ride offers (GET request).
        """
        response = self.client().get('/api/v1/rides/',
                                     headers=({"auth_token": self.generate_token()}))
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
        response = self.client().get('/api/v1/rides/1',
                                     headers=({"auth_token": self.generate_token()}))
        self.assertEqual(response.status_code, 200)
        self.assertIn("ride", response.json)
        self.assertIn("result retrieved successfully", response.json["message"])
        self.assertIsInstance(response.json['ride'], dict)
        self.assertEqual(len(response.json['ride']), 6)

    def test_ride_attributes_returned(self):
        """
        Test that all values expected  in a ride dictionary are returned
        """
        response = self.client().get('/api/v1/rides/1',
                                     headers=({"auth_token": self.generate_token()}))
        self.assertIn(1, response.json['ride'].values())
        self.assertIn("Ntinda", response.json['ride']["destination"])
        self.assertEqual(2, response.json['ride']["number_of_passengers"])
        self.assertEqual(self.depart_date, response.json['ride']["departure_date"])
        self.assertEqual(self.depart_time, response.json['ride']["departure_time"])

    def test_ride_not_found(self):
        """
        Test API returns nothing when a ride is not found
        A return contsins a status code of 200
        """
        response = self.client().get('/api/v1/rides/20',
                                     headers=({"auth_token": self.generate_token()}))
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
            self.ride1.__dict__), content_type='application/json',
                                headers=({"auth_token": self.generate_token()}))

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
            self.ride1.__dict__), content_type='text/plain',
                                      headers=({"auth_token": self.generate_token()}))

        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json)
        self.assertEqual("content not JSON", response.json['error_message'])

    def test_empty_attributes_not_sent(self):
        """
        This method tests that data is not sent with empty fields
        """
        response = self.client().post('/api/v1/rides/', data=json.dumps(
            dict(user_id=2,
                 destination="Mbarara",
                 departure_date="", departure_time="",
                 number_of_passengers=2)), content_type='application/json',
                 headers=({"auth_token": self.generate_token()}))

        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json)
        self.assertEqual("Some fields are empty", response.json['error_message'])

    def test_partial_fields_not_sent(self):
        """
        This method tests that data with partial fields is not send
        on creating a ride offer
        """
        response = self.client().post('/api/v1/rides/', data=json.dumps(
            dict(destination="Mbarara", number_of_passengers=2)),
                                      content_type='application/json',
                                      headers=({"auth_token": self.generate_token()}))
        self.assertEqual(response.status_code, 400)
        self.assertEqual("some of these fields are missing",
                         response.json['error_message'])

    def test_post_joins_a_ride_offer(self):
        """
        This method tests the joinig of a ride offer
        (POST request)
        """

        response = self.client().post('/api/v1/rides/1/requests', data=json.dumps(
            self.request.__dict__), content_type='application/json',
                                      headers=({"auth_token": self.generate_token()}))

        self.assertEqual(response.status_code, 201)
        self.assertIn("request", response.json)
        self.assertEqual("request sent successfully", response.json['message'])
        self.assertTrue(response.json['request'])

    def test_non_json_request_not_sent(self):
        """
        This method tests that non json request is not sent
        """
        response = self.client().post('/api/v1/rides/1/requests', data=json.dumps(
            self.request.__dict__), content_type='text/plain',
            headers=({"auth_token": self.generate_token()}))
        self.assertEqual(response.status_code, 400)
        self.assertEqual("content not JSON", response.json['error_message'])

    def test_empty_request_attributes(self):
        """
        This method tests that data is not sent with empty fields
        """
        response = self.client().post('/api/v1/rides/1/requests', data=json.dumps(
            dict(user_id="", ride_id="")), content_type='application/json',
            headers=({"auth_token": self.generate_token()}))

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
            self.request.__dict__), content_type='application/json',
                                      headers=({"auth_token": self.generate_token()}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual("No ride available with id: 22", response.json['message'])

    def test_partial_request_sent(self):
        """
        This method tests that data with partial fields is not send
        on creating a ride offer
        """
        response = self.client().post('/api/v1/rides/1/requests', data=json.dumps(
            dict(passenger_contact=self.user_test.phone_number)),
                                      content_type='application/json',
                                      headers=({"auth_token": self.generate_token()}))
        self.assertEqual(response.status_code, 400)
        self.assertEqual("some of these fields are missing",
                         response.json['error_message'])

    def test_api_gets_all_ride_requests(self):
        """
        Test API can get all ride requests (GET request).
        """
        response = self.client().get('/api/v1/users/rides/1/requests',
                                   headers=({"auth_token": self.generate_token()}))
        self.assertEqual(response.status_code, 200)
        self.assertIn("result retrieved successfully", response.json["message"])

    def tearDown(self):
        sql_commands = (
            """DROP TABLE IF EXISTS "user" CASCADE;""",
            """DROP TABLE IF EXISTS "ride" CASCADE;""",
            """DROP TABLE IF EXISTS "request" CASCADE;""")
        conn = None
        try:
            conn = DatabaseAccess.database_connection()
            cur = conn.cursor()
            for sql_command in sql_commands:
                cur.execute(sql_command)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
