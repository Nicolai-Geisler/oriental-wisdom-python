# Import Python HTTP module
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
# Import utilities
import random
import time
import os
import json
# Importing the PIL library for image manipulation
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Server class
class MyServer(BaseHTTPRequestHandler):

    def do_POST(self):

        print("Received POST")

        filename = os.path.basename(self.path)
        file_length = int(self.headers['Content-Length'])

        with open(filename, 'wb') as output_file:
            output_file.write(self.rfile.read(file_length))

        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()
        
        self.wfile.write('Image saved','utf-8')


    def do_GET(self):

        match self.path:
            case '/':
                homepage(self)
            case '/api/get-image1':
                print('Get image')
                getImage(self)
            case '/api/get-image2':
                print('Get image')
                getImage(self)
            case '/api/get-quote':
                print('Get quote')
                getQuote(self)
            case '/api/get-final?dark=True&fancy=True' | '/api/get-final?dark=False&fancy=False' | '/api/get-final?dark=True&fancy=False' | '/api/get-final?dark=False&fancy=True':
                print('Get final')
                # Extract query parameters
                query = urlparse(self.path).query
                query_params = parse_qs(query)
                dark = query_params.get("dark", None)  # Get the value of the "dark" parameter
                fancy = query_params.get("fancy", None) # Get the value of the "fancy" parameter
                getFinal(self, dark, fancy)
            case _:
                print('Not found')
                pageNotFound(self)
            
        
# Handle different URLS

# /
def homepage(self):
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    with open('./index.html', 'rb') as file: 
        self.wfile.write(file.read())

# Get Image
def getImage(self):
    self.send_response(200)
    self.send_header("Content-type", "image/jpeg")
    self.end_headers()

    with open('./images/' + getRandomImage(), 'rb') as file: 
        self.wfile.write(file.read())

# Get Quote
def getQuote(self):
    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()

    # Select a random quote
    random_quote = random.choice(quotes_list)
    global currentQuote # Overwrite global variable
    currentQuote = random_quote

    # Send the random quote
    self.wfile.write(bytes(str(random_quote).replace("'", "\""), "utf-8"))
    
# Get Final
def getFinal(self, dark, fancy):

    dark = str(dark).replace("['","")
    dark = str(dark).replace("']","")
    fancy = str(fancy).replace("['","")
    fancy = str(fancy).replace("']","")

    print("Params: dark=" + str(dark) + ", fancy=" + str(fancy))

    self.send_response(200)
    self.send_header("Content-type", "image/png")
    self.end_headers()

    # Open an Image
    img = Image.open('./images/' + currentImage)
    
    # Get quote and author
    quote = currentQuote["quote"]
    author = currentQuote["author"]

    # Set font and size
    font_path = "./fonts/Roboto-Regular.ttf"
    font_size = 70
    if str(fancy) == "True":
        font_path = "./fonts/Fancy.ttf"
        font_size = 75
    
    font_color = 255
    if str(dark) == "True":
        font_color = 0

    font = ImageFont.truetype(font_path, font_size)
    
    # Set maximum width for each line
    max_line_width = 20

    # Wrap text into lines
    lines = textwrap.wrap(quote, width=max_line_width)

    # Position to start adding text
    x, y = img.width / 2, (img.height - sum(font_size for line in lines)) // 3 # img.height / 3

    # Create a new transparent image with the same size as the original
    if str(dark) == "True":
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
    combined.save('output.png')

    with open('./output.png', 'rb') as file: 
        self.wfile.write(file.read())


# Error 404
def pageNotFound(self):
    self.send_response(404)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    self.wfile.write(bytes("<html><head><title>Oriental Wisdom Backend</title></head>", "utf-8"))
    self.wfile.write(bytes("<h1>Page not found</h1>", "utf-8"))
    self.wfile.write(bytes("<a href='/' style='font-size: 20px'>Go to homepage</a>", "utf-8"))

# Functionality

def getAllQuotes():
    # Open the JSON file
    with open('./quotes/quotes.json', 'r') as f:
        data = json.load(f)
    # Return quotes in a list
    return data.get('quotes', [])

def getRandomImage():
    # Get all images from folder
    pictures = []
    for pic in os.listdir('./images/'):
        if pic.endswith(".jpg"):
            pictures.append(pic)

    # Select a random image as response
    picture = random.choice(pictures)
    global currentImage # Overwrite global variable
    currentImage = picture
    return picture


# Global variables
currentImage = getRandomImage()
quotes_list = getAllQuotes()
currentQuote = random.choice(quotes_list)

hostname = "localhost"
port = 8000

if __name__ == "__main__":        
    webServer = HTTPServer((hostname, port), MyServer)
    print("Server started http://%s:%s" % (hostname, port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
