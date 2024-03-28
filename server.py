from flask import Flask, render_template, request
import boto3
import os
import signal

app = Flask(__name__, template_folder='./templates')

# AWS S3 configuration
AWS_REGION = 'us-west-1'
S3_BUCKET_NAME = 'e-bike-images'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    print("upload called")
    if 'fileInput' not in request.files:
        return 'No file part', 400
    
    file = request.files['fileInput']
    
    if file.filename == '':
        return 'No selected file', 400

    # Save the uploaded file temporarily
    uploaded_file_path = '/tmp/' + file.filename
    file.save(uploaded_file_path)

    # Upload the file to S3
    s3_client = boto3.client('s3', region_name=AWS_REGION)
    s3_key = 'images/' + file.filename 
    s3_client.upload_file(uploaded_file_path, S3_BUCKET_NAME, s3_key)

    # Delete the temporary file
    os.remove(uploaded_file_path)

    return 'Image uploaded successfully to S3', 200
    

if __name__ == '__main__':
    print("In main")
    app.run(host='0.0.0.0', port=8090)
