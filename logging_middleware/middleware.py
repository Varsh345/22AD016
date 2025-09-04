from flask import request
from datetime import datetime

def log_request_response(app):
    """Attach logging for requests and response"""
    @app.before_request
    def log_in_request():
        print(f"[{datetime.now()}] Request:{request.method} {request.path}")
    @app.after_request
    def log_out_request(resp):
        print(f"[{datetime.now()}] Request: {resp.status}")
        return resp 