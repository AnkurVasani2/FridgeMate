from flask import Flask, send_file
import firebase_admin
from firebase_admin import credentials, storage
import os
import datetime

app = Flask(__name__)

# Initialize Firebase app
cred = credentials.Certificate("F:\MY_PROJECT\credentials.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'fridgematee.appspot.com'
})
bucket = storage.bucket()

def get_latest_image():
    # List all blobs in the bucket
    blobs = bucket.list_blobs()
    # Filter images based on your naming convention or metadata
    image_blobs = [blob for blob in blobs if blob.name.lower().endswith(('.jpg', '.jpeg'))]
    # Sort images by creation time (assumes timestamp in filename)
    sorted_images = sorted(image_blobs, key=lambda x: x.time_created, reverse=True)
    if sorted_images:
        # Return the name of the latest image
        return sorted_images[0].name
    else:
        return None

@app.route('/get_latest_image')
def get_latest_image_route():
    # Get the name of the latest image
    latest_image_name = get_latest_image()
    if latest_image_name:
        # Specify the path to the latest image in Firebase Storage
        blob = bucket.blob(latest_image_name)
        # Download the image to a temporary file
        temp_image_filename = f"{latest_image_name}"
        blob.download_to_filename(temp_image_filename)
        # Serve the latest image file
        return send_file(temp_image_filename, mimetype='image/jpeg')
    else:
        return "No image found"

if __name__ == "__main__":
    app.run(debug=True)