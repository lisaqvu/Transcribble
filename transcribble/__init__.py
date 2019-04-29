import os

from flask_environments import Environments
from flask import request, Flask, render_template
from google.cloud import storage
import logging
import yaml, json

from . import db 

with open('././app.yaml') as f:
    envfile = yaml.safe_load(f)

#def create_app(config, debug=False, testing=False, config_overrides=None):
def create_app(config):
    # create and configure the app
    # app = Flask(__name__, instance_relative_config=True)

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    # # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    app = Flask(__name__)
    app.config.from_object(config)

    # app.debug = debug
    # app.testing = testing

    # if config_overrides:
    #     app.config.update(config_overrides)

    # # Configure logging
    # if not app.testing:
    #     logging.basicConfig(level=logging.INFO)
    # hacky fix
    app.config.update(envfile['env_variables'])
    os.environ.update(envfile['env_variables'])

    CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']

    @app.route('/')
    def index():
        # return render_template("base.html")
        return render_template("upload.html")

    # HELPER TO GET NEXT ID FROM SQL

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

        # Create a new blob and upload the file's content.
        blob = bucket.blob(uploaded_file.filename)

        blob.upload_from_string(
            uploaded_file.read(),
            content_type=uploaded_file.content_type
        )

        # The public URL can be used to directly access the uploaded file via HTTP.
        return blob.public_url
    with app.app_context():
        model = get_model()
        model.init_app(app)

    @app.route('/edit')
    def edit():
        return render_template("edit.html")

        # [START init_app]
    # Initalize the OAuth2 helper.
    oauth2.init_app(
        app,
        scopes=['email', 'profile'],
        authorize_callback=_request_user_info)
    # [END init_app]

    # [START logout]
    # Add a logout handler.
    @app.route('/logout')
    def logout():
        # Delete the user's profile and the credentials stored by oauth2.
        del session['profile']
        session.modified = True
        oauth2.storage.delete()
        return redirect(request.referrer or '/')
    # [END logout]

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

def get_model():
    from . import db
    return model    

# [START request_user_info]
def _request_user_info(credentials):
    """
    Makes an HTTP request to the Google OAuth2 API to retrieve the user's basic
    profile information, including full name and photo, and stores it in the
    Flask session.
    """
    http = httplib2.Http()
    credentials.authorize(http)
    resp, content = http.request(
        'https://www.googleapis.com/oauth2/v3/userinfo')

    if resp.status != 200:
        current_app.logger.error(
            "Error while obtaining user profile: \n%s: %s", resp, content)
        return None
    session['profile'] = json.loads(content.decode('utf-8'))

# [END request_user_info]    