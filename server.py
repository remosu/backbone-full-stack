import json
import pymongo
from bson.objectid import ObjectId
from bson import json_util

from flask import Flask, render_template, request, make_response

app = Flask(__name__)

app.debug = True

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/todos/', defaults={'todo_id': None})
@app.route('/todos/<todo_id>',  methods=['GET','POST','PUT','DELETE'])
def todos_api(todo_id):
    method = request.method
    body = None
    
    if method == 'GET':
        body = get_todos(todo_id)
    
    resp = make_response(json.dumps(body, default=json_util.default))
    resp.mimetype = 'application/json'
    
    return resp

def get_todos(todo_id):
    db = get_db()
    todo = db.todos.find_one({'_id': ObjectId(todo_id)})
    todo['id'] = str(todo['_id'])
    del todo['_id']
    
    return todo

def save_todo():
    pass

def update_todo():
    pass

def delete_todo(todo_id):
    pass

def get_db():
    conn = pymongo.Connection('localhost', 27017)
    return conn.todos_db

if __name__ == '__main__':
    app.run(host='0.0.0.0')
