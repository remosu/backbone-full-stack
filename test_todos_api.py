import json
import requests
import unittest
from pymongo import Connection
from multiprocessing import Process
from server import app

port = 5001
url = 'http://localhost:%s' % port

def start_server():
    app.db_name = 'todos_test'
    app.debug = False
    app.run(port=port)

def make_request(path, data):
    return requests.post(url + path, data=json.dumps(data), 
        headers={'Content-Type': 'application/json'})

class TodoApiIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_process = Process(target=start_server)
        cls.server_process.start()
    
    @classmethod
    def tearDownClass(cls):
        cls.server_process.terminate()
        
        conn = Connection('localhost', 27017)
        conn.drop_database('todos_test')
        conn.disconnect()
    
    def test_create_todo(self):
        resp = make_request('/todos/', {'text': 'foo', 'order': 1, 'done': False})
        
        self.assertEquals(200, resp.status_code)
        
        data = json.loads(resp.content)
        
        self.assertIn('id', data)

