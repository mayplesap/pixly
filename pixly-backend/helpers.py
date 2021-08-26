import os
import boto3
from config import S3_KEY, S3_SECRET, S3_LOCATION, S3_BUCKET
from PIL import Image, ImageOps
from models import db, Pixly


ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'tiff', 'svg'}
IMAGE_PATH = "./images/"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)


def upload_file_to_s3(file, bucket_name, acl="public-read"):

    try: 
        s3.upload_fileobj(  #  s3.upload_fileobj
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    
    except Exception as e:
        print("Something went wrong: ", e)
        return e
    
    return "{}{}".format(S3_LOCATION, file.filename)


def upload_backend_file_to_s3(filepath, bucket_name, acl="public-read"):
    filename = filepath.split("/")[-1]
    extension = filepath.split(".")[-1]
    
    if extension == "jpg":
        extension = "jpeg"
    
    try: 
        s3.upload_file(  #  s3.upload_fileobj
            filepath,
            bucket_name,
            filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": (f"image/{extension}")
            }
        )
    
    except Exception as e:
        print("Something went wrong: ", e)
        return e
    
    return "{}{}".format(S3_LOCATION, filename)

def fetch_image_link_from_db(id):
    link = db.session.query(Pixly.img_link).filter(Pixly.id == id).one()[0]
    return link

def fetch_image_file_from_bucket(link): 
    filename = link.split("/")[-1]
    s3.download_file(S3_BUCKET, filename, f'{IMAGE_PATH}{filename}')
    return (f'{IMAGE_PATH}{filename}')

def convert_to_black_and_white(imagePath):
    image = Image.open(imagePath)
    greyscale_image = image.convert('L')
    greyscale_image.save(imagePath)

    # link = upload_backend_file_to_s3(imagePath, S3_BUCKET) 
    # os.remove(imagePath)
    # return str(link)




