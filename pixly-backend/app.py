"""Flask app for Pixly"""
import os
import pdb
import boto3

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pixly
# from secret import ACCESS_KEY, SECRET_KEY
from config import S3_BUCKET, S3_KEY, S3_LOCATION, S3_SECRET
from helpers import s3, upload_file_to_s3, allowed_file, convert_to_black_and_white, fetch_image_file_from_bucket, upload_backend_file_to_s3, convert_sepia, convert_to_color_merge
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
db.create_all()




##############################################################################

# @app.route("/api/images")
# def show_images():
#     """TODO: NAME PENDING
#     Get data of all images. Respond with JSON like:
#     ..."""

# @app.route("/api/images", methods=["GET"])
# def show_image():
#     """TODO: docstrings"""
#     image = Pixly.query.get(1)
#     print("IMAGE", image)
#     print("IMAGE LINK?", image.img_link)
#     im = Image.open(image.img_link)
#     print("IM", im)
#     color = "green"
#     border = (20,10,20,10)
#     new_img = ImageOps.expand(im, border=border, fill=color)
#     return new_img

@app.route("/image/bw", methods=["POST"])
def back_and_white_image():
    """TODO: docstrings"""
    print("REQUEST DATA", request.data.decode("UTF-8"))
    link = request.data.decode("UTF-8")
    image_path = fetch_image_file_from_bucket(link)
    convert_to_black_and_white(image_path)
    bw_link = upload_backend_file_to_s3(image_path, S3_BUCKET)
    os.remove(image_path)
    return str(bw_link)

@app.route("/image/sepia", methods=["POST"])
def sepia_image():
    """TODO: docstrings"""
    link = request.data.decode("UTF-8")
    image_path = fetch_image_file_from_bucket(link)
    convert_sepia(image_path)
    sepia_link = upload_backend_file_to_s3(image_path, S3_BUCKET)
    os.remove(image_path)
    return str(sepia_link)

@app.route("/image/merge", methods=["POST"])
def color_merge_image():
    """TODO: docstrings"""
    link = request.data.decode("UTF-8")
    image_path = fetch_image_file_from_bucket(link)
    convert_to_color_merge(image_path)
    color_merge_link = upload_backend_file_to_s3(image_path, S3_BUCKET)
    os.remove(image_path)
    return str(color_merge_link)

@app.route("/", methods=["POST"])
@cross_origin()
def upload_file():
    """TODO: docstrings"""
    if "file" not in request.files:
        return "No user_file key in request.files"

    file = request.files["file"]
    # below variables for database
    uploadedBy = request.form["uploadedBy"]
    category = request.form["category"]
    name = request.form["name"]

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

        new_image = Pixly(name=name,
                      category=category,
                      uploaded_by=uploadedBy,
                      img_link=str(output))
        db.session.add(new_image)
        db.session.commit()
        return str(output)

    else: 
        pass


