import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, request
from util import make_json_response, bad_id_response

app = Flask(__name__)

app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/todos/', methods=['GET'])
def get_todos():
    todos = get_collection()
    cur = todos.find().sort('order', pymongo.ASCENDING)
    data = []
    
    for todo in cur:
        todo['id'] = str(todo['_id'])
        del todo['_id']
        data.append(todo)
    
    return make_json_response(data)

@app.route('/todos/<todo_id>',  methods=['GET'])
def get_todo(todo_id):
    oid = None
    
    try:
        oid = ObjectId(todo_id)
    except:
        return bad_id_response()
    
    todos = get_collection()
    todo = todos.find_one({'_id': oid})
    
    if todo is None:
        return make_json_response({'message': 'no todo with id: ' + todo_id}, 404)
    
    todo['id'] = str(todo['_id'])
    del todo['_id']
    
    return make_json_response(todo)

@app.route('/todos/', methods=['POST'])
def create_todo():
    data = request.json
    todos = get_collection()
    oid = todos.insert(data)
    todo = todos.find_one({'_id': ObjectId(oid)})
    todo['id'] = str(todo['_id'])
    del todo['_id']
    return make_json_response(todo)

@app.route('/todos/<todo_id>',  methods=['PUT'])
def update_todo(todo_id):
    data = request.json
    todos = get_collection()
    todos.update({'_id': ObjectId(todo_id)}, {'$set': data})
    return make_json_response({'message': 'OK'})

@app.route('/todos/<todo_id>',  methods=['DELETE'])
def delete_todo(todo_id):
    todos = get_collection()
    todos.remove(ObjectId(todo_id))
    return make_json_response({'message': 'OK'})

def get_collection():
    conn = pymongo.Connection('localhost:27017', **app.conn_args)
    return conn[app.db_name].todos

if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('-r', '--replicaset', dest='replicaset', help='Define replicaset name to connect to.')
    
    options, args = parser.parse_args()
    
    if options.replicaset is not None:
        app.conn_args = {'replicaset': options.replicaset, 'slave_okay': True}
    else:
        app.conn_args = {}
    
    app.db_name = 'todos_prod'
    app.run(host='0.0.0.0')
