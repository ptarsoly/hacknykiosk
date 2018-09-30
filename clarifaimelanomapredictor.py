from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import sys
import os
import json
from google.cloud import storage


storage_client = storage.Client.from_service_account_json('googlecreds.json')

with open('credentials.json', 'r') as f:
    creds = json.load(f)


##account_sid = creds["twilio"]["account_sid"]
##auth_token  = creds["twilio"]["auth_token"]
api_key = creds["clarifai"]["api_key"]

##imageurl = sys.argv[1]

name = 'candidate.jpg'

bucket = storage_client.get_bucket('melanomadetector')

os.system("sudo google_speech 'capture complete. uploading file '")

destination_blob_name = name
source_file_name = name

blob = bucket.blob(destination_blob_name)

blob.upload_from_filename(source_file_name)
blob.make_public()

print('File {} uploaded to {}.'.format(source_file_name, destination_blob_name))


imageurl = 'https://storage.googleapis.com/melanomadetector/candidate.jpg'

app = ClarifaiApp(api_key=api_key)

model = app.models.get('melanomadetector')
model.model_version = 'd472e3e2fab84c698de67c47dfeb1123'

image = ClImage(url=imageurl)

os.system("sudo google_speech 'upload complete. analyzing '")

output = model.predict([image])

print (output)

print ('----------')


##jsonres = json.loads(output)
jsonout = {}

jsonout["melanoma"] = output["outputs"][0]["data"]["concepts"][2]["value"]
jsonout["typical"] = output["outputs"][0]["data"]["concepts"][1]["value"]
jsonout["atypical"] = output["outputs"][0]["data"]["concepts"][0]["value"]

if jsonout["melanoma"] > jsonout["typical"] and jsonout["melanoma"] > jsonout["atypical"] :
    jsonout["prediction"] = "melanoma"
else :
    jsonout["prediction"] = "notmelanoma"

print (jsonout)

with open('prediction.json', 'w') as outfile:
    json.dump(jsonout, outfile)



