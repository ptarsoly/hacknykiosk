from flask import Flask, request, redirect
import requests
import io
import sys
import os
import json
from twilio.twiml.voice_response import Record, VoiceResponse, Say
from twilio.twiml.messaging_response import MessagingResponse
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import translate
##from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

recordingurl = ''

@app.route("/answer", methods=['GET', 'POST'])
def answer_call():
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.say("Thank you for calling the New York alert hotline. Please record your alert message at the beep. Press the star key to end.", voice='alice')
    resp.record(
    action='http://0b95747f.ngrok.io/data',
    method='GET',
    max_length=40,
    finish_on_key='*')

    resp.hangup()

    
    
    return str(resp)

@app.route("/data", methods=['GET', 'POST'])
def get_data():
    print('---------------------------')
    recordingurl = request.args.get('RecordingUrl')
    print (recordingurl)
    print('---------------------------')

    resp2 = VoiceResponse()
    resp2.say('thank you')
    resp2.hangup()

    print('-------------translate-part--------------')
    
    r = requests.get(recordingurl, allow_redirects=True)
    open('recording.wav', 'wb').write(r.content)

    client = speech.SpeechClient.from_service_account_json('googlecreds.json')
    translate_client = translate.Client.from_service_account_json('googlecreds.json')

    #translate whatever is found to english
    target = 'en' 

    with io.open('recording.wav', 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)


    ##audio = types.RecognitionAudio(uri=recordingurl)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code='en-US')

    response = client.recognize(config, audio)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        text = result.alternatives[0].transcript
        with open('transcript.txt', 'w') as the_file:
            the_file.write(text)

        translation = translate_client.translate(text, target_language=target)
        print(u'Translation: {}'.format(translation['translatedText']))
        with open('translation.txt', 'w') as the_file2:
            the_file2.write(translation['translatedText'])


    
    return (str(resp2))

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response

    textmsg = request.values.get('Body', None)
    print("------------------")
    print(textmsg)
    print("------------------")

    
    url = "https://api.giphy.com/v1/gifs/search"

    querystring = {"api_key":"a53jHN8htoVbAoShauJAmJRwfxttgA4k","q":textmsg,"limit":"1","offset":"0","rating":"R","lang":"en"}

    headers = {
        'Cache-Control': "no-cache",
        'Postman-Token': "60a96ddf-6f0f-441a-a947-c25093610d9e"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    jsonres = json.loads(response.text)

    mediaurl = jsonres["data"][0]["images"]["fixed_width"]["url"]

    print (mediaurl)

    
    resp = MessagingResponse()

    # Add a message
    msg = resp.message("Thank you for your notification! heres a gif for the occasion!")

    msg.media(mediaurl)
    

    return str(resp)



if __name__ == "__main__":
    ##app.run(debug=True, port = 8001)
    app.run(debug=True, host = '169.62.204.155', port = 8001)
