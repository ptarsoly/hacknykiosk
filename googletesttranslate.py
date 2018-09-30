from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import translate



client = speech.SpeechClient.from_service_account_json('googlecreds.json')

#translate whatever is found to english
target = 'en' 


recordingurl = 'https://api.twilio.com/2010-04-01/Accounts/AC252e4eb8a1214bbb8af6b120886c6cc2/Recordings/RE47aeac8558bc28e72c29d8322dc858a3'


audio = types.RecognitionAudio(uri=recordingurl)
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

