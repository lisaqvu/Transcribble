# Transcribble

Transcribble is a simple web editor for automatic transcribing and translating of audio and video files

## Set up development environment

Transcribble is built with Python Flask, for more information on how to set up the enviroment, check out [here](http://flask.pocoo.org/docs/1.0/quickstart/). The `requirements.txt` file includes all the necessary packages for the app.

In order to run the application on your virtual environment, run
```
   $ export FLASK_APP=transcribble
   $ export FLASK_ENV=development
   $ python -m flask run
```

## Running individual files

Before you begin, set up GCLOUD_APPLICATION_CREDENTIALS from the terminal and set up your   CLOUD_STORAGE_BUCKET in the app.yaml file. 

### Parsing Files
Transcribble support 3 types of files: subtitle (\*.srt), audio (\*.wav), and video files

If the audio extensions are not supported, use the methods `parseAudio('[PATH_TO_FILE])` in Parse.py to parse the file to \*.wav. The new file will be included in `/temp_files/` folder within the current directory.

### SpeechToText.py
The `speechToText` function accept the uri input in the format `gs://[GCLOUD_STORAGE_BUCKET]/[FILE_NAME]`

Make sure that your input file is a **wav** file. Then go to SpeechToText.py and run `speechToText('[FILE_URL]')`. You can also change the language to one that is supported by Google API (the list of all the available languages is in TranscriptionLangs.json). It might take a while, but the response is a dictionary for further usage.

We also have a test file available at `gs://transcribble/test.wav`

SpeechToText.py includes a utility function calls `parseTranscription` that will parse the response into a Transcription object that will be used throughout the app.

### Translate.py
After getting the Transcription object from speechToText, go to Translate.py and use the `translate([TRANSCRIPTION_OBJECT], [ORIGINAL_LANGUAGE], [TARGET_LANGUAGE])`. The list of all supported languages is in TranslationLangs.json.

The result will be a new Transcription (this is a misnomer) object.

### Export 
There is an export method within each Transcription object. Simply call `[TRANSCRIPTION_OBJECT].srt(file_name, dir)`. The extension of file_name must be explicitly declared (.srt/.txt).

There is an ExportToZip.py that allows the user to get all the files that they were working with as a zip file.

### Other files
endpoints, export, LangSelection are helpers file for the front end of the app.





