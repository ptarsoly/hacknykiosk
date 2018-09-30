import sys
import time
import json
import requests
from twilio.rest import Client

with open('credentials.json', 'r') as f:
    creds = json.load(f)


account_sid = creds["twilio"]["account_sid"]
auth_token  = creds["twilio"]["auth_token"]

##print (account_sid)
##print (auth_token)

client = Client(account_sid, auth_token) 

sender = sys.argv[1]
receiver = sys.argv[2]
text = " ".join(sys.argv[3:len(sys.argv)])


url = "https://api.giphy.com/v1/gifs/search"

querystring = {"api_key":"a53jHN8htoVbAoShauJAmJRwfxttgA4k","q":text,"limit":"1","offset":"0","rating":"R","lang":"en"}

headers = {
    'Cache-Control': "no-cache",
    'Postman-Token': "60a96ddf-6f0f-441a-a947-c25093610d9e"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

jsonres = json.loads(response.text)

mediaurl = jsonres["data"][0]["images"]["fixed_width"]["url"]

print (mediaurl)



message = client.messages.create( 
                              from_=sender,  
                              body=text,
                              media_url=mediaurl,
                              to=receiver 
                          )



print(message.sid)

