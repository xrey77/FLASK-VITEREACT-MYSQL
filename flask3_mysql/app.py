import os
from config import create_app, db
from datetime import datetime
from flask import Flask, Blueprint, redirect,jsonify, url_for, request, send_from_directory, make_response
from flask_cors import CORS, cross_origin

app = Flask(__name__) 
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# app = Flask(__name__, static_url_path='', static_folder='vite-react/build')
# CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'        
# app.secret_key = os.environ.get('SECRET')



# @app.route("/", defaults={'path':''})
# @cross_origin('*')
# def serve(path):
#     return send_from_directory(app.static_folder,'index.html')

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
    
    