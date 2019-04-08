from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
	return 'Index Page'

@app.route('/<int:projectid>')
def show_project(project_id):
	#id for each project
    return 'Project %s' % project_id