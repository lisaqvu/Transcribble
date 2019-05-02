import os

from flask_environments import Environments
from flask import request, Flask, session, render_template, redirect, Response
from google.cloud import storage
import logging
import yaml, json
from . import Translate, Transcription, SpeechToText
#from . import db

#import httplib2

# from oauth2client.contrib.flask_util import UserOAuth2

# oauth2 = UserOAuth2()

with open('././app.yaml') as f:
    envfile = yaml.safe_load(f)
with open('././TranslationLangs.json') as json_file:  
    langs = json.load(json_file)

def create_app(config):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(config)

    # hacky fix
    app.config.update(envfile['env_variables'])
    os.environ.update(envfile['env_variables'])

    CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']

    @app.route('/')
    def index():
        # return render_template("base.html")
        return render_template("upload.html")


    @app.route('/upload', methods=['POST'])
    def upload():
        """Process the uploaded file and upload it to Google Cloud Storage."""
        uploaded_file = request.files.get('file')

        if not uploaded_file:
            return 'No file uploaded.', 400

        # Create a Cloud Storage client.
        gcs = storage.Client()

        # Get the bucket that the file will be uploaded to.
        bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)


        # if (file_extension != 'wav'):
        #     uploaded_file = AudioFileClip(uploaded_file)

        # Create a new blob and upload the file's content.
        blob = bucket.blob(uploaded_file.filename)

        blob.upload_from_string(
            uploaded_file.read(),
            content_type=uploaded_file.content_type
        )

        file_name = uploaded_file.filename
        file_name, file_extension = os.path.splitext(file_name)
        session['link'] = blob.public_url
        url = blob.public_url.replace('https://storage.googleapis.com/', 'gs://')
        output = SpeechToText.speechToText(url)
        parsedfile = SpeechToText.parseTranscription(output)
        session['file'] = parsedfile.getDict()
        session['name'] = file_name
        return render_template("edit.html", filelink = session['link'], filename=file_name, dict_object=parsedfile.getDict(), langlist=langs)

    @app.route("/edit", methods=['POST'])
    def edit():
        current = Transcription.makeObjectFromForm(request.form.to_dict())
        current_as_dict = current.getDict()
        session['file'] = current_as_dict
        if "update" in request.form:
            return render_template("edit.html", filelink = session['link'], filename=session['name'], dict_object=current_as_dict, langlist=langs)

        elif "export" in request.form:
            return redirect("/download")

    @app.route("/translate", methods=['POST'])
    def translate():
        target = request.form['languagePicker']
        parsedfile = Transcription.makeObjectFromDict(session.get('file'))
        translated = Translate.translator(parsedfile, target)

        translated_as_dict = translated.getDict()
        session['file'] = translated_as_dict
        file_name=session['name']
        return render_template("edit.html", filelink = session['link'], filename=file_name, dict_object=translated_as_dict, langlist=langs)
    
    @app.route("/download", methods=["GET"])
    def download():
        current = session['file']
        srt = Transcription.makeObjectFromDict(current).srt()
        print(srt)

        return Response(
        srt,
        mimetype="text/srt",
        headers={"Content-disposition":
                 ("attachment; filename=" + session["name"]+".srt")})
    @app.errorhandler(500)
    def server_error(e):
        logging.exception('An error occurred during a request.')
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    @app.errorhandler(403)
    def permission_error(e):
        return render_template("403.html")

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html")


    if __name__ == '__main__':
        # This is used when running locally. Gunicorn is used to run the
        # application on Google App Engine. See entrypoint in app.yaml.
        app.run(host='127.0.0.1', port=8080, debug=True)

    return app

