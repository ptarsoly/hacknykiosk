import sys
import os
from twilio.twiml.voice_response import VoiceResponse, Say
from google.cloud import storage

# Explicitly use service account credentials by specifying the private key
# file.
storage_client = storage.Client.from_service_account_json('googlecreds.json')


message = " ".join(sys.argv[1:len(sys.argv)-1])
soundurl = sys.argv[len(sys.argv)-1]

print (message)
print (soundurl)


response = VoiceResponse()
response.say(message, voice='alice')
response.play('https://api.twilio.com/cowbell.mp3', loop=1)

print(response)

out = str(response)

file = open("voiceresponse.xml", "w")
file.write(out)
file.close()

bucket = storage_client.get_bucket('hackny')
destination_blob_name = 'voiceresponse.xml'
source_file_name = 'voiceresponse.xml'

blob = bucket.blob(destination_blob_name)
blob.content_type = 'application/xml'

blob.upload_from_filename(source_file_name)
blob.make_public()

print('File {} uploaded to {}.'.format(source_file_name, destination_blob_name))


