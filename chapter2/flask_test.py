'''
   Cloud Native Python - Chapter 02 - Building the Unit testing

    nose = Unit Testing Framework:  pip install nose
        To run it execute nosetests from a terminal window
        within the same flask_test.py's path
'''

from app import app
import unittest

class FlaskappTest(unittest.TestCase):
    def setUp(self):
        # Test the app and initialize self.app with our app
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_users_status_code(self):
        # sends HTTP GET request to the app (/api/v1/users)
        result = self.app.get('/api/v1/users')
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
    
    def test_tweets_status_code(self):
        # sends HTTP GET request to the app (/api/v2/tweets)
        result = self.app.get('/api/v2/tweets')
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        
    def test_apiinfo_status_code(self):
        # sends HTTP GET request to the application
        result = self.app.get('/api/v1/info')
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
    
    def test_addusers_status_code(self):
        # sends HTTP POST request ('/api/v1/users')
        result = self.app.post('/api/v1/users', data='{"username":"test_usr", "email":"tusr@test.local", "password":"test543"}', content_type='application/json')
        print (result)
        # assert the status code of the response
        self.assertEqual(result.status_code, 201)

    def test_updusers_status_code(self):
        # sends HTTP PUT request ('/api/v1/users/<int: id>')
        result = self.app.put('/api/v1/users/21', data='{"password":"testing123"}', content_type='application/json')
        print (result)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_addtweets_status_code(self):
        # sends HTTP POST request ('/api/v2/tweets')
        result = self.app.post('/api/v2/tweets', data='{"username":"test_usr","body":"Wow It works! #testing"}', content_type='application/json')
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
    
    def test_delusers_status_code(self):
        # sends HTTP Delete request ('/api/v1/users') for specific usr
        result = self.app.delete('/api/v1/users', data='{"username":"test_usr"}', content_type='application/json')
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
