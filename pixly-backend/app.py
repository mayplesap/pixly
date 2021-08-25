"""Flask app for Pixly"""
import os
import pdb
import boto3

from PIL import Image
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db
# from secret import ACCESS_KEY, SECRET_KEY
from config import S3_BUCKET, S3_KEY, S3_LOCATION, S3_SECRET
from helpers import s3, upload_file_to_s3, allowed_file
from werkzeug.utils import secure_filename 

app = Flask(__name__)
CORS(app)
database_url = os.environ.get('DATABASE_URL', 'postgresql:///pixly')

# fix incorrect database URIs currently returned by Heroku's pg setup
database_url = database_url.replace('postgres://', 'postgresql://')

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)



##############################################################################

# @app.route("/api/images")
# def show_images():
#     """TODO: NAME PENDING
#     Get data of all images. Respond with JSON like:
#     ..."""

# @app.route("/api/images/<int:image_id>")
# def show_image():
#     """TODO: NAME PENDING
#     Get data of a image. Respond with JSON like:
#     ..."""

@app.route("/", methods=["POST"])
def upload_file():

    if "user_file" not in request.files:
        return "No user_file key in request.files"

    file = request.files["user_file"]

    """
        These attributes are also available

        file.filename               # The actual name of the file
        file.content_type
        file.content_length
        file.mimetype

    """

    if file.filename == "":
        return "Please select a file"

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, S3_BUCKET)
        print(S3_BUCKET, "THIS IS THE BUCKET NAME FROM APP")
        print("THIS IS THE OUTPUT FROM APP",output)
        return str(output)

    else: 
        pass