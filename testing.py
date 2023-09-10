import io
import os
import json
from werkzeug.utils import secure_filename
import unittest
from flask import Flask, request, jsonify
from bson import ObjectId

app = Flask(__name__)
UPLOAD_FOLDER = 'static'  # Folder to store uploaded images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'jfif'}  # Allowed file extensions for images
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_image', methods=['POST'])
def upload_image():
    image = request.files.get('image')
    if image and allowed_file(image.filename):
        # filename = secure_filename(image.filename)
        filename = f"{ObjectId()}.{image.filename}"
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"message": "Image uploaded successfully.", "filename": filename}), 200
    else:
        return jsonify({"message": "Invalid image or file format."}), 400

# Mock method to create a valid image (e.g., a JPEG image)
def create_valid_image():
    # Create a BytesIO object and write valid image data (e.g., JPEG) to it
    valid_image_data = b'\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xFF\xDB\x00\x43\x00\x08...'
    return io.BytesIO(valid_image_data)

# Mock method to create an invalid image (e.g., a text file)
def create_invalid_image():
    # Create a BytesIO object and write invalid data (e.g., text) to it
    invalid_image_data = b'This is not an image file.'
    return io.BytesIO(invalid_image_data)

class TestUploadImage(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()  # Create a test client

    def test_valid_image_upload(self):
        # Specify the path to your desired image file
        image_path = r'C:\Users\Administrator\Desktop\pic\sheldon-6HMdrAlt8IQ-unsplash.jpg'

        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        # Extract the filename from the path
        filename = os.path.basename(image_path)

        response = self.app.post(
            '/upload_image',
            data={'image': (io.BytesIO(image_data), filename)},
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "Image uploaded successfully.")
        # Add more assertions as needed

    def test_invalid_image_upload(self):
        # Create a temporary invalid image (e.g., by providing invalid image data)
        invalid_image_data = b'This is not an image file.'
        invalid_filename = 'invalid_image.txt'

        response = self.app.post(
            '/upload_image',
            data={'image': (io.BytesIO(invalid_image_data), invalid_filename)},
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "Invalid image or file format.")
        # Add more assertions as needed


if __name__ == '__main__':
    unittest.main()
