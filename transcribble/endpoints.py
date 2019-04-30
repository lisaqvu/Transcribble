from flask_cors import CORS
from flask import Flask, json, g, request
import os

import oauth2, get_model, storage
import upload, transcribe, translate, edit, export

app = Flask(__name__)
CORS(app)

@app.route("/parse", methods=["GET"])
@oauth2.required
def parse(bucket_name, audio_file = None, video_file = None, srt_file = None, start_time = -1, end_time = -1):
    if audio_file is not None:
        parseAudio(audio_file, bucket_name, start_time=start_time, end_time=end_time)
    if video_file is not None:
        parseVideo(video_file, bucket_name, start_time=start_time, end_time=end_time)
    if srt_file is not None:
        trans = parseSrt(srt_file, bucket_name)
        if not path.exists(r'./temp_files'):
            os.mkdir(r'./temp_files')
        trans.storeRaw('Transcription.json', r'./temp_files')

@app.route("/transcribe", methods=["GET", "POST"])
@oauth2.required
def transcribe(audio_uri, lang = 'en-US', speaker_num = 1):
    assert request.method == 'GET'
    response = speechToText(audio_uri, lang = lang, speaker_num = speaker_num)
    trans = parseTranscription(response)
    if not path.exists(r'./temp_files'):
        os.mkdir(r'./temp_files')
    trans.storeRaw('Transcription.json', r'./temp_files')
def get_transcription():
    assert request.method == 'GET'
    f = open(r'./temp_files/Transcription.json', 'r')
    res = json.load(f.read())
    return json_response(res)
def store_transcription(json_dict):
    trans = recoverRawJson(json_dict)
    trans.storeRaw('Transcription.json', r'./temp_files')

@app.route("/translate", methods=["GET"])
@oauth2.required
def translate(transcription, lang1, lang2):
    assert request.method == 'GET'
    trans = Translate.translate(transcription, lang1, lang2)
    trans.storeRaw('Translation.json', r'./temp_files')
def get_translation():
    assert request.method == 'GET'
    f = open(r'./temp_files/Translation.json', 'r')
    res = json.load(f.read())
    return json_response(res)


@app.route("/export", methods=["GET"])
@oauth2.required
def export():
    if not path.exists(r'./temp_files'):
        os.mkdir(r'./temp_files')
    trans.srt('Transcription.srt', r'./temp_files')

def json_response(payload, status=200):
 return (json.dumps(payload), status, {'content-type': 'application/json'})