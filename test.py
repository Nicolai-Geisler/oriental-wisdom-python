# Import Flask webserver
import urllib.request
from flask import Flask, request, send_file, json, make_response
# Import utilities
import random
import time
import os
import json
import urllib
# Importing the PIL library for image manipulation
from PIL import Image, ImageDraw, ImageFont
import textwrap


app = Flask(__name__)

# Functionality
def getAllQuotes():
    # Open the JSON file
    with open('./quotes/quotes.json', 'r') as f:
        data = json.load(f)
    # Return quotes in a list
    return data.get('quotes', [])

def getRandomImage():

    # Use fallback if no unsplash images are available
    directory = './images/unsplash/'
    if os.listdir('./images/unsplash/') == []:
        directory = './images/'

    # Get all images from folder
    pictures = []
    for pic in os.listdir(directory):
        if pic.endswith(".jpg"):
            pictures.append(pic)

    # Select a random image as response
    picture = random.choice(pictures)
    global currentImage # Overwrite global variable

    # make shure the same image is not beeing send twice in a row
    while currentImage == picture:
        picture = random.choice(pictures)
    
    currentImage = picture

    return directory + picture

def createSharepic(dark, fancy):
    # Open an Image
    img = Image.open(currentImage)
    
    # Get quote and author
    quote = currentQuote["quote"]
    author = currentQuote["author"]

    # Set font and size
    font_path = "./fonts/Roboto-Regular.ttf"
    font_size = 80
    if str(fancy) == "true":
        font_path = "./fonts/Fancy.ttf"
        font_size = 85
    
    font_color = 255
    if str(dark) == "false":
        font_color = 0

    font = ImageFont.truetype(font_path, font_size)
    
    # Set maximum width for each line
    max_line_width = 20

    # Wrap text into lines
    lines = textwrap.wrap(quote, width=max_line_width)

    # Position to start adding text
    x, y = img.width / 2, (img.height - sum(font_size for line in lines)) // 3 # img.height / 3

    # Create a new transparent image with the same size as the original
    if str(dark) == "false":
        txt_img = Image.new('RGBA', img.size, (255, 255, 255, 50))
    else:
        txt_img = Image.new('RGBA', img.size, (0, 0, 0, 100))

    # Create a drawing object
    draw = ImageDraw.Draw(txt_img)

    # Add each line of text
    for line in lines:
        draw.text((x, y), line, fill=(font_color, font_color, font_color), font=font, anchor="mm", align="center")
        y += font_size  # Move down for the next line
    
    font = ImageFont.truetype(font_path, 50)
    draw.text((x * 0.9, y + font_size), '- ' + author, fill=(font_color, font_color, font_color), font=font)

    # Combine the two images
    combined = Image.alpha_composite(img.convert("RGBA"), txt_img)
    
    # Save the edited image
    combined.save('images/output.png')

    # return the file
    return 'images/output.png'

def getUnsplashImages():
    
    print("Getting Unsplash images...")

    # URL parameters for unsplash API
    baseUrl = 'https://api.unsplash.com/photos/random'
    clientID = 'Ixp2xDIRS_6ocXQM0FMTii6OTjAPoCdyBRMUbp4MUxI'
    count = 1
    queries = ['nature', 'zen', 'landscape', 'asia']

    # Download 10 images
    i = 1
    while i <= 10:
        response = urllib.request.urlopen(baseUrl + '?client_id=' + clientID + '&count=' + str(count) + '&orientation=squarish&query=' + random.choice(queries))

        response_body = response.read()

        data = json.loads(response_body.decode("utf-8"))

        imageUrls = ""
        imageUrl = ""
        imageName = "image"

        for image in data:
            imageName = image['id']
            imageUrls = image['urls']
            imageUrl = imageUrls['regular']

            imageName = "images/unsplash/" + imageName + ".jpg"
            urllib.request.urlretrieve(imageUrl, imageName)

        i += 1
    
    return True

# API endpoints

@app.route('/api/get-quote', methods=['GET'])
def send_quote():
    print("Received GET QUOTE request")

    random_quote = random.choice(quotes_list)
    global currentQuote # Overwrite global variable
    currentQuote = random_quote

    response = app.response_class(
        response=json.dumps(random_quote),
        mimetype='application/json'
    )

    return response, 200

@app.route('/api/get-image1', methods=['GET'])
def send_image_one():
    print("Received GET request")

    file = getRandomImage()
    try:
        
        return send_file(file, mimetype='image/jpeg')
    except Exception as e:
        return str(e), 500
    
@app.route('/api/get-image2', methods=['GET'])
def send_image_two():
    print("Received GET request")

    file = getRandomImage()
    try:

        return send_file(file, mimetype='image/jpeg')
    except Exception as e:
        return str(e), 500

@app.route('/api/get-final', methods=['GET'])
def send_sharepic():
    print("Received GET FINAL request")

    dark = request.args.get('dark')
    fancy = request.args.get('fancy')
    print("Params: dark: " + str(dark) + ", fancy: " + str(fancy))

    file = createSharepic(dark, fancy)
    try:

        return send_file(file, mimetype='image/png')
    except Exception as e:
        return str(e), 500

@app.route('/upload', methods=['POST'])
def upload_image():

    print("Received POST request")
    try:
        # Get the image data from the request
        image_data = request.data

        # Process the image (e.g., save it to disk)
        # You can also decode base64-encoded images if needed
        # print(image_data)

        with open("request.jpg", 'wb') as f:
            f.write(image_data)

        # Return a success response
        return "Image uploaded successfully!", 200
    except Exception as e:
        return str(e), 500

# fetch images
getUnsplashImages()

# Global variables
currentImage = ""
currentImage = getRandomImage()
quotes_list = getAllQuotes()
currentQuote = random.choice(quotes_list)

# Start the webserver
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)