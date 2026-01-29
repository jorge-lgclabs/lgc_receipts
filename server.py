import os.path
import json
from flask import Flask, render_template, request, flash, url_for
from werkzeug.utils import redirect
from PIL import Image
from functions import extract_datetime, date_rewrite

UPLOAD_FOLDER = 'to_be_uploaded'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = b'a3%TgB#\"Mo1z\n\xd5/?'
app.config[UPLOAD_FOLDER] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pre-process', methods=["post"])
def pre_process_date():
    incoming_filename = f'pre_process/{request.files['file'].filename}'
    request.files['file'].save(incoming_filename)

    result = extract_datetime(incoming_filename)

    return result

@app.route('/', methods=["post"])
def post():
    date = request.form['entered_date']
    vendor = request.form['name'].replace(" ", "_")
    amount = request.form['amount']
    category = request.form['category']
    photo = request.files['photo']
    photo_filename = photo.filename
    extension = photo_filename.split(".")[-1]

    if extension in ALLOWED_EXTENSIONS:
        filepath = f'{UPLOAD_FOLDER}/{date}-{vendor.replace(" ", "_")}-{amount}.{extension}'

        resize_image = Image.open(photo)
        resize_image.thumbnail((1300, 1300))
        resize_image.save(filepath)

        flash(f'{filepath} successfully saved ', 'success')
    else:
        flash('Please select image file (.png, .jpg, .jpeg)', 'error')
        return redirect(url_for('home'))

    date_rewrite_result = date_rewrite(date, filepath)
    if date_rewrite_result:
        flash(f'{date}-{vendor.replace(" ", "_")}.{extension} date successfully changed', 'success')
    else:
        flash('There was an error while changing the date of the file', 'error')


    return redirect(url_for('home'))


app.run(debug=True)