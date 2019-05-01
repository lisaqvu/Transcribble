from .Transcription import *
from google.cloud import translate as gcloud

def translator(transcription, lang1, lang2):
    client = gcloud.Client()
    trans = Transcription([],[])
    for sentence in transcription.sentences():
        content = client.translate(sentence.content(),source_language = lang1, target_language = lang2)
        content = content['translatedText']
        new = Sentence(sentence.timestamp(), content, speaker_tag = sentence.speakerTag())
        trans.appendSentence(new)

    return trans