import os.path
import json
from flask import Flask, render_template, request, flash
from functions import extract_datetime

UPLOAD_FOLDER = 'to_be_uploaded'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
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
        photo.save(os.path.join(app.config[UPLOAD_FOLDER], f'{vendor}-{date}.{extension}'))
    meta_dict = {}
    meta_dict['vendor'] = vendor
    meta_dict['date'] = date
    meta_dict['amount'] = amount
    meta_dict['category'] = category

    with open(f'{UPLOAD_FOLDER}/{vendor}-{date}.json', 'w') as file:
        json.dump(meta_dict, file, indent=4)



    #flash('que es esto')

    return f"{date}, {vendor}, {amount}, {category}"


app.run(debug=True)