from os.path import abspath, dirname, join
import mimetypes
from flask import Flask, request, make_response

app_resources = join(abspath(dirname(__file__)),'..','static')

app = Flask(__name__, static_folder=app_resources)

@app.route('/<path:resource>')
def serve_test_resource(resource):
    mtype, encoding = mimetypes.guess_type(resource)
    
    with app.open_resource(resource) as f:
        contents = f.read()
        resp = make_response(contents)
        resp.mimetype = mtype
        return resp

def run_server():
    app.run(host='0.0.0.0', debug=True)

if __name__ == '__main__':
    run_server()
