import os
import time
from flask import Flask, render_template, request, send_from_directory
from PIL import Image, ImageFilter

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/processed'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')

        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', error='No selected file')

        if file:
            filename = f"{int(time.time())}_{file.filename}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            filter_type = request.form.get('filter')

            img = Image.open(filepath)

            if filter_type == 'grayscale':
                img = img.convert('L')
            elif filter_type == 'blur':
                img = img.filter(ImageFilter.BLUR)
            elif filter_type == 'contour':
                img = img.filter(ImageFilter.CONTOUR)
            elif filter_type == 'detail':
                img = img.filter(ImageFilter.DETAIL)
            elif filter_type == 'edge_enhance':
                img = img.filter(ImageFilter.EDGE_ENHANCE)
            elif filter_type == 'sharpen':
                img = img.filter(ImageFilter.SHARPEN)

            processed_filename = f"edited_{filename}"
            processed_path = os.path.join(PROCESSED_FOLDER, processed_filename)
            img.save(processed_path)

            return render_template('index.html',
                                   original=filename,
                                   processed=processed_filename)

    return render_template('index.html')


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(PROCESSED_FOLDER, filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=5000)