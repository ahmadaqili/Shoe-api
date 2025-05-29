from flask import Flask, request, jsonify
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return '''
    <h2>آپلود تصویر کفش</h2>
    <form method="POST" action="/predict" enctype="multipart/form-data">
        <input type="file" name="image">
        <input type="submit" value="ارسال">
    </form>
    '''

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'فایل ارسال نشده'}), 400
    
    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'نام فایل معتبر نیست'}), 400

    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    try:
        img = Image.open(image_path)
        img.verify()  # اعتبارسنجی اولیه
    except Exception as e:
        return jsonify({'error': 'فایل تصویر معتبر نیست', 'detail': str(e)}), 400

    # پاسخ تستی
    return jsonify({
        'message': 'تصویر با موفقیت دریافت شد',
        'filename': image.filename,
        'brand': 'نایک (تخمینی)',
        'model': 'Air Force 1',
        'color': 'سفید با لوگو مشکی'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)