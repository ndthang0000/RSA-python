# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
import bcrypt
import uuid
import os
import datetime

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# img = Image.open("static/upload/52785b27-aafc-4ae8-a5bf-f590664b4766.png")
# print(img)
# new_img = img.filter(ImageFilter.GaussianBlur(radius=5))
# new_img.show()


mongodb_client = PyMongo(app, uri="mongodb+srv://phamnguyet:nguyetchuot.12@cluster0.w4fcj.mongodb.net/test")
db = mongodb_client.db

@app.route('/api/upload', methods=['POST'])
def upload():
    file_to_upload = request.files['image']
    extension = os.path.splitext(file_to_upload.filename)[1]
    f_name = str(uuid.uuid4()) + extension
    file_to_upload.save(os.path.join('static/upload', f_name))
    return jsonify({'success': True})


@app.route('/api/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    name = request.json['name']

    user = db.user.find_one({"username": username})
    hash_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(5))
    if user:
        return jsonify(success=False, message='Username đã tồn tại')
    db.user.insert_one({'username': username,
                        'password': hash_password,
                        'name': name,
                        'createdAt': datetime.datetime.now()
                        })
    return jsonify(success=True)

@app.route('/api/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user = db.user.find_one({"username": username})
    if user:
        if bcrypt.checkpw(password.encode(), user['password']):
            return jsonify(success=True)
        return jsonify(success=False, message='Mật khẩu không chính xác')
    return jsonify(success=False, message='Tài khoản không tồn tại')

if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
