import json
from bson import json_util
from flask import make_response

def make_json_response(body, status_code):
    resp = make_response(json.dumps(body, default=json_util.default))
    resp.status_code = status_code
    resp.mimetype = 'application/json'
    
    return resp
