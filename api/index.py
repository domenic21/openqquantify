from http.server import BaseHTTPRequestHandler
import sys
import os
from urllib.parse import urlparse, parse_qs
import json

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template
from ai_routes import ai_routes

app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')
app.register_blueprint(ai_routes)

@app.route('/')
def index():
    return render_template('index.html')

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        with app.test_client() as client:
            response = client.get(self.path)
            
            self.send_response(response.status_code)
            for header, value in response.headers:
                if header.lower() != 'content-length':
                    self.send_header(header, value)
            self.send_header('Content-Length', str(len(response.data)))
            self.end_headers()
            self.wfile.write(response.data)
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b''
        
        with app.test_client() as client:
            response = client.post(
                self.path,
                data=post_data,
                headers=dict(self.headers)
            )
            
            self.send_response(response.status_code)
            for header, value in response.headers:
                if header.lower() != 'content-length':
                    self.send_header(header, value)
            self.send_header('Content-Length', str(len(response.data)))
            self.end_headers()
            self.wfile.write(response.data)
