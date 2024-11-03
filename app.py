import flask
import os
import sys
import utils
from dotenv import load_dotenv
from typing import Tuple

app = flask.Flask(__name__)

# Folder where uploaded files will be saved
load_dotenv(".env")
SITE_INDEX = os.getenv("SITE_INDEX")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
UPLOAD_ROUTE = os.getenv("UPLOAD_ROUTE")
UPLOADS_ROUTE = os.getenv("UPLOADS_ROUTE")

ENV_VARS = (SITE_INDEX, UPLOAD_FOLDER, UPLOAD_ROUTE, UPLOADS_ROUTE)
utils.check_env(ENV_VARS)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER      

# Route to show the main page
@app.route(SITE_INDEX)
def index() -> str:
  files = os.listdir(app.config['UPLOAD_FOLDER'])
  return flask.render_template('index.html', files=files)

# Route to handle file uploads
@app.route(UPLOAD_ROUTE, methods=['POST'])
def upload_file() -> flask.Response:
  if 'file' not in flask.request.files:
    return flask.redirect(flask.url_for('index'))
  file = flask.request.files['file']
  if file.filename == '':
    return flask.redirect(flask.url_for('index'))
  if file:
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return flask.redirect(flask.url_for('index'))

# Route to see the uploaded files
@app.route(f"{UPLOADS_ROUTE}/<filename>")
def uploaded_file(filename) -> flask.Response:
  return flask.send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0", port=5000)