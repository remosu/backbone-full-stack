import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, request
from util import make_json_response

app = Flask(__name__)

app.debug = True

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/todos/', defaults={'todo_id': None}, methods=['GET','POST'])
@app.route('/todos/<todo_id>',  methods=['GET','DELETE'])
def todos_api(todo_id):
    method = request.method.upper()
    body = None
    status_code = 200
    
    if todo_id is not None:
        try:
            todo_id = ObjectId(todo_id)
        except:
            return make_json_response({'message': 'bad id'}, 400)
    
    if method == 'GET':
        body = get_todos(todo_id)
        
        if body is None:
            status_code = 404
    
    elif method == 'DELETE':
        body = delete_todo(todo_id)
    else:
        body = {'error': 'no method found'}
    
    return make_json_response(body, status_code)

def get_todos(todo_id):
    todos = get_collection()
    todo = todos.find_one({'_id': todo_id})
    
    if todo is None:
        return None
    
    todo['id'] = str(todo['_id'])
    del todo['_id']
    
    return todo

@app.route('/todos/', methods=['POST'])
def save_todo():
    data = request.json
    todos = get_collection()
    oid = todos.insert(data)
    return make_json_response({'id': str(oid)}, 200)

@app.route('/todos/<todo_id>',  methods=['PUT'])
def update_todo(todo_id):
    data = request.json
    todos = get_collection()
    todos.update({'_id': ObjectId(todo_id)}, {'$set': data})
    return make_json_response({'message': 'OK'}, 200)

def delete_todo(todo_id):
    todos = get_collection()
    todos.remove(todo_id)
    return {'message': 'OK'}

def get_collection():
    conn = pymongo.Connection('localhost', 27017)
    return conn[app.db_name].todos

if __name__ == '__main__':
    app.db_name = 'todos_prod'
    app.run(host='0.0.0.0')
