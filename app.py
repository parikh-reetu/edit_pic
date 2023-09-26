from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import atexit
import os
import shutil
from filters import pixelate_image

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# clear all uploads when app is closed


@atexit.register
def clear_folder():
    folder_path = app.config['UPLOAD_FOLDER']
    if os.path.exists(folder_path):
        # Remove all files and subdirectories in the folder
        shutil.rmtree(folder_path)
        # Recreate the folder to ensure it exists
        os.makedirs(folder_path)


# home page to upload photo


@app.route('/')
def index():
    return render_template('home.html')


# when the upload button from the home page is clicked, this route checks if a
# file has been uploaded, and if it has we redirect to the page where you can
# modify the photo
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return redirect(url_for('modify', filename=file.filename))


@app.route('/modify/<filename>', methods=['GET', 'POST'])
def modify(filename):
    return render_template('modify.html', filename=filename)


@app.route('/pixelate/<filename>', methods=['POST'])
def pixelate(filename):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    slider_value = int(request.form['slider_value'])
    print(slider_value)

    pixelated_image = pixelate_image(image_path, slider_value)
    modified_filename = f'modified_{filename}'
    modified_image_path = os.path.join(
        app.config['UPLOAD_FOLDER'], modified_filename)
    pixelated_image.save(modified_image_path)
    return redirect(url_for('modified', filename=modified_filename))


# TODO add more filters

@app.route('/modified/<filename>', methods=['GET'])
def modified(filename):
    return render_template('modified.html', filename=filename)


if __name__ == '__main__':
    app.run(debug=True)
