import html
import io
import os

import json


# Imports the Google Cloud client libraries
from google.oauth2 import service_account
from google.api_core.exceptions import AlreadyExists
from google.cloud import texttospeech
from google.cloud import translate_v3beta1 as translate
from google.cloud import vision

creds = service_account.Credentials.from_service_account_file('../../credentials/BadukNewsAPI-ab5d90acd1e9.json.nogit')
    

def pic_to_text(infile):
    """Detects text in an image file

    ARGS
    infile: path to image file

    RETURNS
    String of text detected in image
    """

    # Instantiates a client
    client = vision.ImageAnnotatorClient(credentials=creds)

    # Opens the input image file
    with io.open(infile, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # For dense text, use document_text_detection
    # For less dense text, use text_detection
    response = client.document_text_detection(image=image)
    text = response.full_text_annotation.text
    print("Detected text: {}".format(text))

    return response