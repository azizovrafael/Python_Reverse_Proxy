from flask import Flask
from flask import Flask,request,redirect,Response
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SITE_NAME = 'https://localhost:5000/'


@app.route("/")
def index():
    """Serve the default index page."""
    return "Hello World!"


@app.route('/<path:path>',methods=['GET'])
def proxya(path):
	if request.method=='GET':
		resp = requests.get(f'{SITE_NAME}{path}', verify='aspnetapp.crt')
		excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
		headers = [(name, value) for (name, value) in     resp.raw.headers.items() if name.lower() not in excluded_headers]
		response = Response(resp.content, resp.status_code, headers)
	return response

@app.route('/<path:path>',methods=['POST'])
def proxy(path):
	if request.method=='POST':
		resp = requests.post(f'{SITE_NAME}{path}',json=request.get_json(), verify='aspnetapp.crt')
		excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
		headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
		response = Response(resp.content, resp.status_code, headers)
	return response

if __name__ == "__main__":
    """Ensure Flask listens on all interfaces."""
    app.run(host='0.0.0.0', port="8001")
