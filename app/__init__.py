from flask import Flask

app = Flask(__name__)

from app import routes
from app.SETTINGS import ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


app.run(debug=True)