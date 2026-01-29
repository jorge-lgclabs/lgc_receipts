import os.path
from flask import Flask, render_template, request, flash, url_for
from werkzeug.utils import redirect
from PIL import Image
from functions import extract_datetime, date_rewrite, spreadsheet_writer

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

    # filetype check
    if extension not in ALLOWED_EXTENSIONS:
        flash('Please select image file (.png, .jpg, .jpeg)', 'error')
        return redirect(url_for('home'))

    #  resize image, give it vendor-amount filename, save it to upload folder
    filepath = f'{UPLOAD_FOLDER}/{date}-{vendor}-{amount}.{extension}'

    resize_image = Image.open(photo)
    resize_image.thumbnail((1300, 1300))
    resize_image.save(filepath)

    flash(f'{filepath} successfully saved ', 'success')

    #  change modified date of newly saved image to the date entered on form
    date_rewrite_result = date_rewrite(date, filepath)
    if date_rewrite_result:
        flash(f'{date}-{vendor.replace(" ", "_")}.{extension} date successfully changed', 'success')
    else:
        flash('There was an error while changing the date of the file', 'error')

    #  write result to spreadsheet
    spreadsheet_write_result = spreadsheet_writer(date, vendor, amount, category)
    if spreadsheet_write_result:
        flash(f'{date}-{vendor} was successfully added to the spreadsheet', 'success')
    else:
        flash('There was an error while adding entry to the spreadsheet', 'error')

    #  delete the pre-processed file
    for filename in os.listdir('pre_process'):
        os.remove(f'pre_process/{filename}')

    return redirect(url_for('home'))


app.run(debug=True)