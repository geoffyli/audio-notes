import assemblyai as aai
from pprint import pprint
import json

aai.settings.api_key = "0d3d110e7c34441c83126e4e5a74cdf6"

# URL of the file to transcribe
FILE_URL = "test.m4a"

# create a Transcriber object
transcriber = aai.Transcriber()

# transcribe the file
transcript = transcriber.transcribe(FILE_URL)
sentences = transcript.get_sentences()
for sentence in sentences:
    pprint(sentence.start)
    pprint(sentence.end)
    pprint(sentence)
    print("=========================================================================")
pprint(len(sentences))