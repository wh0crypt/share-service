import flask
import os
import sys
from dotenv import load_dotenv
from typing import Tuple

app = flask.Flask(__name__)

# Folder where uploaded files will be saved
load_dotenv(".env")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
if UPLOAD_FOLDER is None:
  print("UPLOAD_FOLDER not set in .env file")
  sys.exit(1)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route to show the main page
@app.route('/')
def index():
  files = os.listdir(app.config['UPLOAD_FOLDER'])
  return flask.render_template('index.html', files=files)

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
  if 'file' not in flask.request.files:
    return flask.redirect(flask.url_for('index'))
  file = flask.request.files['file']
  if file.filename == '':
    return flask.redirect(flask.url_for('index'))
  if file:
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return flask.redirect(flask.url_for('index'))

# Route to see the uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
  return flask.send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
  app.run(debug=True)
