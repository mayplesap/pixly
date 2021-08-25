"""Flask app for Pixly"""
import os
import pdb
import boto3

from PIL import Image
from flask import Flask, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db
from secret import ACCESS_KEY, SECRET_KEY

app = Flask(__name__)

database_url = os.environ.get('DATABASE_URL', 'postgresql:///pixly')

# fix incorrect database URIs currently returned by Heroku's pg setup
database_url = database_url.replace('postgres://', 'postgresql://')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

# Let's use Amazon S3
# s3 = boto3.client(
#         's3',
#         'us-west-1',
#         aws_access_key_id=ACCESS_KEY,
#         aws_secret_access_key=SECRET_KEY
#     )
s3 = boto3.resource('s3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY)
bucket = "sk-rithm-pixly"
# bucket = 
file_name = "./ozzy.jpg"
key_name = "ozzy.jpg"

# with open('oz.jpg','rb') as data:
#     bucket.upload_fileobj(data, 'mykey')

# Upload a new file to bucket
s3.meta.client.upload_file(file_name, bucket, key_name, ExtraArgs={"ACL":"public-read",
                                                                  "ContentType": "image/jpeg"})

# data = open('test.jpg', 'rb')
# s3.Bucket('my-bucket').put_object(Key='test.jpg', Body=data)


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

# @app.route("/api/images", methods=["POST"])
# def upload_image():
#     """TODO: NAME PENDING
#     Upload new image. Respond with JSON like:
#     ..."""


#     s3 = boto3.client(
#         's3',
#         'us-west-1',
#         aws_access_key_id=ACCESS_KEY,
#         aws_secret_access_key=SECRET_KEY
#     )
#     bucket = "sk-rithm-pixly"
#     file_name = "oz.jpg"
#     key_name = "oz"

    # Upload a new file to bucket
    # s3.upload_file(file_name, bucket, key_name)
    # data = open('oz.jpg', 'rb')
    # s3.Bucket('sk-rithm-pixly').put_object(Key='oz.jpg', Body=data)
