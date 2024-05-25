from flask import Flask, request, send_file, make_response

app = Flask(__name__)

@app.route('/api/get-quote', methods=['GET'])
def send_quote():
    print("Received GET QUOTE request")

    return '{ "quote": "Some useless quote about something", "author": "Some Name" }', 200

@app.route('/api/get-image1', methods=['GET'])
def send_image_one():
    print("Received GET request")

    file = 'images/ricefield.jpg'
    try:
        
        return send_file(file, mimetype='image/jpeg')
    except Exception as e:
        return str(e), 500
    
@app.route('/api/get-image2', methods=['GET'])
def send_image_two():
    print("Received GET request")

    file = 'images/waterfall.jpg'
    try:

        return send_file(file, mimetype='image/jpeg')
    except Exception as e:
        return str(e), 500

@app.route('/api/get-final', methods=['GET'])
def send_sharepic():
    print("Received GET FINAL request")

    file = 'images/buddha.jpg'
    try:

        return send_file(file, mimetype='image/jpeg')
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)