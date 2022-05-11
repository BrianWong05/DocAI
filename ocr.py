from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

import os
import time
from dotenv import load_dotenv
load_dotenv()

'''
Authenticate
'''
key = os.getenv("AZURE_OCR_KEY")
endpoint = os.getenv("AZURE_OCR_ENDPOINT")

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))
'''
END - Authenticate
'''

class OCR():
    def OCR_URL(url):
        response = computervision_client.read(url,  raw=True)
        return response

    def OCR_FILE(path):
        file = open(path, "rb")
        response = computervision_client.read_in_stream(file,  raw=True)
        return response

    def GET_TEXT_FROM_FILE(file):
        response = OCR.OCR_FILE(file)
        operation_location = response.headers["Operation-Location"]
        operation_id = operation_location.split("/")[-1]
        while True:
            result = computervision_client.get_read_result(operation_id)
            if result.status not in ['notStarted', 'running']:
                break
            time.sleep(1)

        return_text = ''
        if result.status == OperationStatusCodes.succeeded:
            for text_result in result.analyze_result.read_results:
                for line in text_result.lines:
                    print(line.text)
                    return_text += line.text

        return return_text

    def GET_TEXT_FROM_URL(url):
        response = OCR.OCR_FILE(url)
        operation_location = response.headers["Operation-Location"]
        operation_id = operation_location.split("/")[-1]
        while True:
            result = computervision_client.get_read_result(operation_id)
            if result.status not in ['notStarted', 'running']:
                break
            time.sleep(1)

        return_text = ''
        if result.status == OperationStatusCodes.succeeded:
            for text_result in result.analyze_result.read_results:
                for line in text_result.lines:
                    print(line.text)
                    return_text += line.text

        return return_text