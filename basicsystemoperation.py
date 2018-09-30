from flask import Flask, request, redirect, Response, json
import requests
import io
import time
import datetime
import sys
import os
import json
import subprocess
##from twilio.twiml.voice_response import Record, VoiceResponse, Say
##from twilio.twiml.messaging_response import MessagingResponse
##from google.cloud import speech
##from google.cloud.speech import enums
##from google.cloud.speech import types
##from google.cloud import translate
##from twilio.twiml.voice_response import VoiceResponse
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

recordingurl = ''

@app.route("/step1", methods=['GET', 'POST'])
def step1():
    os.system("sudo google_speech 'capturing image, standby'")

    filename = time.strftime("%H-%M") + "_" + time.strftime("%d-%m-%Y")
    picturefilename = filename +".jpg"

    print (picturefilename)

    print (datetime.datetime.now().isoformat())

    datetimestamp = datetime.datetime.now().isoformat()

    ##take a picture

    commandstring = "sudo raspistill -w 800 -h 600 -t 2 -o " + picturefilename
    os.system(commandstring)
    commandstring = "sudo cp " + picturefilename + " candidate.jpg"
    os.system(commandstring)

    os.system("sudo python clarifaimelanomapredictor.py blank")

    with open('prediction.json', 'r') as f:
        pred = json.load(f)

    js = json.dumps(pred)

    resp = Response(js, status=200, mimetype='application/json')
    ##resp.headers['Link'] = 'http://google.com'

    return resp


@app.route("/step2", methods=['POST'])
def step2():

    res = request.json

    ##json.dumps(request.json)
    print("------------")
    print (res)

    js = json.dumps(res)

    with open('prediction.json', 'r') as f:
        pred = json.load(f)

    pred["patientNum"] = json.loads(js)["phoneNum"]

    

    os.system("sudo google_speech 'sending analysis results to Doctor Peter Tarsoly '")

    commandstring = "sudo python twiliogenericmmssender.py +13213607501 +16318973828 https://storage.googleapis.com/melanomadetector/candidate.jpg " + json.dumps(pred)

    os.system(commandstring)


    resp = Response(js, status=200, mimetype='application/json')
    ##resp.headers['Link'] = 'http://google.com'

    return resp


if __name__ == "__main__":
    ##app.run(debug=True,  port = 8001)
    app.run(debug=True, host = '192.168.43.83', port = 8002)

