#!/usr/bin/env python

from pymongo import Connection
conn = Connection("localhost:27017", slave_okay=True)

config = {
    '_id': 'foo', 
    'members': [
        {'_id': 0, 'host': 'localhost:27017'},
        {'_id': 1, 'host': 'localhost:27018'},
        {'_id': 2, 'host': 'localhost:27019'}
    ]
}

resp = conn.admin.command("replSetInitiate", config)

print resp

conn.disconnect()
