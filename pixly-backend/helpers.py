import os
import boto3
import math
from config import S3_KEY, S3_SECRET, S3_LOCATION, S3_BUCKET
from PIL import Image, ImageOps, ImageDraw
from models import db, Pixly


ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'tiff', 'svg'}
IMAGE_PATH = "./images/"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#######################################################################
# AWS S3 upload functions
# credit to: https://www.zabana.me/notes/flask-tutorial-upload-files-amazon-s3

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
        s3.upload_file(  
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

# Query database for an image link by id
def fetch_image_link_from_db(id):
    link = db.session.query(Pixly.img_link).filter(Pixly.id == id).one()[0]
    return link

# Get image link from AWS, download the image, and return the image path
def fetch_image_file_from_bucket(link): 
    filename = link.split("/")[-1]
    s3.download_file(S3_BUCKET, filename, f'{IMAGE_PATH}{filename}')
    return (f'{IMAGE_PATH}{filename}')

############################################################################
#FILTERS

# BLACK AND WHITE
def convert_to_black_and_white(imagePath):
    image = Image.open(imagePath)
    greyscale_image = image.convert('L')
    greyscale_image.save(imagePath)


# SEPIA
#
# Credit to: https://www.codementor.io/@isaib.cicourel/intermediate-image-filters-mj6y7abx4
# Create a new image with the given size
def create_image(i, j):
    image = Image.new("RGB", (i, j), "white")
    return image


# Get the pixel from the given image
def get_pixel(image, i, j):
    # Inside image bounds?
    width, height = image.size
    if i > width or j > height:
        return None

    # Get Pixel
    pixel = image.getpixel((i, j))
    return pixel


# Limit maximum value to 255
def get_max(value):
    if value > 255:
        return 255

    return int(value)

# Sepia is a filter based on exagerating red, yellow and brown tones
# This implementation exagerates mainly yellow with a little brown
def get_sepia_pixel(red, green, blue, alpha):
    # Filter type
    value = 0

    # This is a really popular implementation
    tRed = get_max((0.759 * red) + (0.398 * green) + (0.194 * blue))
    tGreen = get_max((0.676 * red) + (0.354 * green) + (0.173 * blue))
    tBlue = get_max((0.524 * red) + (0.277 * green) + (0.136 * blue))

    if value == 1:
        tRed = get_max((0.759 * red) + (0.398 * green) + (0.194 * blue))
        tGreen = get_max((0.524 * red) + (0.277 * green) + (0.136 * blue))
        tBlue = get_max((0.676 * red) + (0.354 * green) + (0.173 * blue))
    
    if value == 2:
        tRed = get_max((0.676 * red) + (0.354 * green) + (0.173 * blue))
        tGreen = get_max((0.524 * red) + (0.277 * green) + (0.136 * blue))
        tBlue = get_max((0.524 * red) + (0.277 * green) + (0.136 * blue))
        

    # Return sepia color
    return tRed, tGreen, tBlue, alpha

# Convert an image to sepia
def convert_sepia(imagePath):
    image = Image.open(imagePath).convert("RGB")

    # Get size
    width, height = image.size

    # Create new Image and a Pixel Map
    new = create_image(width, height)
    pixels = new.load()

    # Convert each pixel to sepia
    for i in range(0, width, 1):
        for j in range(0, height, 1):
            p = get_pixel(image, i, j)
            pixels[i, j] = get_sepia_pixel(p[0], p[1], p[2], 255)

    # Save new image
    new.save(imagePath)



# POINTILIZE

# helper function for pointilize
# Return the color average
def color_average(image, i0, j0, i1, j1):
    # Colors
    red, green, blue, alpha = 0, 0, 0, 255

    # Get size
    width, height = image.size

    # Check size restrictions for width
    i_start, i_end = i0, i1
    if i0 < 0:
        i_start = 0
    if i1 > width:
        i_end = width

    # Check size restrictions for height
    j_start, j_end = j0, j1
    if j0 < 0:
        j_start = 0
    if j1 > height:
        j_end = height

    # This is a lazy approach, we discard half the pixels we are comparing
    # This will not affect the end result, but increase speed
    count = 0
    for i in range(i_start, i_end - 2, 2):
        for j in range(j_start, j_end - 2, 2):
            count+=1
            p = get_pixel(image, i, j)
            red, green, blue = p[0] + red, p[1] + green, p[2] + blue

    # Set color average
    red /= count
    green /= count
    blue /= count

    # Return color average
    return int(red), int(green), int(blue), alpha

# Create a Pointilize version of the image
def convert_pointilize(imagePath):
    image = Image.open(imagePath).convert("RGB")
    # Get size
    width, height = image.size

    # Radius
    radius = 6

    # Intentional error on the positionning of dots to create a wave-like effect
    count = 0
    errors = [1, 0, 1, 1, 2, 3, 3, 1, 2, 1]

    # Create new Image
    new = create_image(width, height)

    # The ImageDraw module provide simple 2D graphics for Image objects
    draw = ImageDraw.Draw(new)

    # Draw circles
    for i in range(0, width, radius+3):
        for j in range(0, height, radius+3):
            # Get the color average
            color = color_average(image, i-radius, j-radius, i+radius, j+radius)
            
            # Set error in positions for I and J
            eI = errors[count % len(errors)]
            count += 1
            eJ = errors[count % len(errors)]

            # Create circle
            draw.ellipse((i-radius+eI, j-radius+eJ, i+radius+eI, j+radius+eJ), fill=(color))

    # Save new image
    new.save(imagePath)


# COLOR MERGE
def convert_to_color_merge(imagePath):
    image = Image.open(imagePath).convert("RGB")
    red, green, blue = image.split()
    new_image = Image.merge("RGB", (green, red, blue))
    new_image.save(imagePath)

# ADD BORDER
# open image
def add_border(imagePath):
    image = Image.open(imagePath)
    # border color
    color = "black"
    # top, right, bottom, left
    border = (20, 20, 20, 20)
    new_img = ImageOps.expand(image, border=border, fill=color)
    # save new image
    new_img.save(imagePath)
###########################################################################