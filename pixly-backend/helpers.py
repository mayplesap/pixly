import boto3
from config import S3_KEY, S3_SECRET, S3_LOCATION

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'tiff', 'svg'}


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
        print(file.filename, "FILE.FILENAME FROM UPLOAD IN HELPERS, And the type is: ", type(file.filename), )
        print(file.content_type, "FILE.CONTENT-TYPE FROM UPLOAD IN HELPERS, and the type is: ", type(file.content_type))
        print(bucket_name, "BUCKET NAME FROM HELPERS")
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