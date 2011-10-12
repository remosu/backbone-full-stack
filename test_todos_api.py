import json
import requests

todo = {'text': 'foo', 'order': 3, 'done': False}

resp = requests.post('http://localhost:5000/todos/', 
    data=json.dumps(todo), 
    headers={'Content-Type': 'application/json'})

print resp.status_code, resp.content
