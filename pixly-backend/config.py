import os
# Grabs environment variables to keep our secrets safe

S3_BUCKET = os.environ.get("S3_BUCKET")
S3_KEY = os.environ.get("S3_KEY")
S3_SECRET = os.environ.get("S3_SECRET")
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

