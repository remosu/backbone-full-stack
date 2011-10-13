import json
import requests
import unittest
from pymongo import Connection
from bson.objectid import ObjectId
from multiprocessing import Process
from server import app

port = 5001
url = 'http://localhost:%s' % port
db_name = 'todos_test'

def start_server():
    app.db_name = db_name
    app.debug = False
    app.run(port=port)

def post(path, data):
    return requests.post(url + path, data=json.dumps(data), 
        headers={'Content-Type': 'application/json'})

class TodoApiIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_process = Process(target=start_server)
        cls.server_process.start()
        cls.conn = Connection('localhost', 27017)
    
    @classmethod
    def tearDownClass(cls):
        cls.server_process.terminate()
        cls.conn.drop_database(db_name)
        cls.conn.disconnect()
    
    def tearDown(self):
        self.conn[db_name].drop_collection('todos')
    
    def test_create_todo(self):
        resp = post('/todos/', {'text': 'foo', 'order': 1, 'done': False})
        
        self.assertEqual(200, resp.status_code)
        
        data = json.loads(resp.content)
        
        self.assertIn('id', data)
        
        todo = self.conn[db_name].todos.find_one({'_id': ObjectId(data['id'])})
        
        self.assertEqual('foo', todo['text'])
    
    def test_get_todo(self):
        todo = {'text': 'foo', 'order': 1, 'done': False}
        create_resp = post('/todos/', todo)
        _id = json.loads(create_resp.content)['id']
        
        resp = requests.get(url + '/todos/' + _id)
        
        self.assertEqual(200, resp.status_code)
        
        data = json.loads(resp.content)
        
        self.assertEqual(data['text'], todo['text'])
        self.assertEqual(data['order'], todo['order'])
        self.assertEqual(data['done'], todo['done'])

