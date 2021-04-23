import os
import unittest
import json

from application import app


class HomeAutomationTestCase(unittest.TestCase):
    def setUp(self):
        """Tnstructions executed before and after each test method. """
        self.app = app
        self.client = self.app.test_client
        app.config['JSON_DATA'] = "data_test.json"
        self.dummyData = {
            "temperature": 75,
            "lights": {
                "1": {
                    "id": "1",
                    "turnedOn": True,
                },
                "2": {
                    "id": "2",
                    "turnedOn": True,
                },
                "3": {
                    "id": "3",
                    "turnedOn": True
                }
            }
        }
        with open(app.config['JSON_DATA'], "w") as jsonFile:
            json.dump(self.dummyData, jsonFile)
    
    def test_get_thermostat(self):
        res = self.client().get('/temperature')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])

    def test_set_thermostat(self):
        res = self.client().post('/temperature', json={"temperature": 70})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['data'], 70)

    def test_400_set_thermostat_invalid(self):
        res = self.client().post('/temperature', json={"temperature": "abc"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],"Bad request")

    def test_get_lights(self):
        res = self.client().get('/lights')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['data']), 3)
    
    def test_get_light_by_ID(self):
        res = self.client().get('/lights/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])
        self.assertEqual(data['data']['id'],"1")

    def test_404_get_light_by_InvalidID(self):
        res = self.client().get('/lights/INVALID')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],"Resource not found")

    def test_create_light_fixture(self):
        res = self.client().post('/lights')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['data']['turnedOn'], False)

    def test_create_light_fixture_increase_light_count(self):
        res = self.client().get('/lights')
        data_before = json.loads(res.data)
        self.client().post('/lights')
        res = self.client().get('/lights')
        data_after = json.loads(res.data)
        self.assertEqual(len(data_before['data']), len(data_after['data'])-1)

    def test_remove_light_fixture(self):
        res = self.client().delete('/lights/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['light_deleted'], "1")
    
    def test_404_remove_light_fixture_InvalidID(self):
        res = self.client().delete('/lights/INVALID')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],"Resource not found")

    def test_remove_light_fixture_decrease_light_count(self):
        res = self.client().get('/lights')
        data_before = json.loads(res.data)
        self.client().delete('/lights/1')
        res = self.client().get('/lights')
        data_after = json.loads(res.data)
        self.assertEqual(len(data_before['data']), len(data_after['data'])+1)

    def test_toggle_light_fixture(self):
        res = self.client().put('/lights/2')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])
        self.assertEqual(data['data']['turnedOn'], False)

    def test_404_if_toggle_light_fixture_fails(self):
        res = self.client().put('/lights/INVALID')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],"Resource not found")
    

if __name__ == "__main__":
    unittest.main()
