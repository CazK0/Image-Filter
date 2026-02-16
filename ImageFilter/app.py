import os
import time
from flask import Flask, render_template, request, send_from_directory
from PIL import Image, ImageFilter, ImageEnhance

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/processed'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    error = None
    processed_filename = None
    original_filename = None

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
            try:
                intensity = float(request.form.get('intensity', 2))
            except ValueError:
                intensity = 2.0
            
            img = Image.open(filepath)
            
            if filter_type == 'grayscale':
                img = img.convert('L')
            elif filter_type == 'blur':
                img = img.filter(ImageFilter.GaussianBlur(radius=intensity))
            elif filter_type == 'sharpen':
                img = img.filter(ImageFilter.UnsharpMask(radius=intensity, percent=150))
            elif filter_type == 'brightness':
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(intensity)
            elif filter_type == 'contrast':
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(intensity)
            elif filter_type == 'contour':
                img = img.filter(ImageFilter.CONTOUR)

            processed_filename = f"edited_{filename}"
            processed_path = os.path.join(PROCESSED_FOLDER, processed_filename)
            img.save(processed_path)

            original_filename = filename

    return render_template('index.html', 
                           original=original_filename, 
                           processed=processed_filename,
                           error=error)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(PROCESSED_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
