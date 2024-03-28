import os
import pytest
import requests
from requests import get, post
from flask import Flask
from io import BytesIO

@pytest.fixture
def client():
    app = Flask(__name__, template_folder='./templates')
    app.config['TESTING'] = True

base_url = 'http://localhost:8090'

def test_index(client):
    response = requests.get(base_url+'/')
    assert response.status_code == 200
    assert 'Upload an Image' in response.text

def test_upload_file(client):
    files = {'fileInput': open('e-bike.png', 'rb')}

    response = requests.post(base_url+'/upload', files=files)

    assert response.status_code == 200
    assert 'Image uploaded successfully to S3' in response.text