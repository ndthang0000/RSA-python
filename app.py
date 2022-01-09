# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from flask import Flask, jsonify, request,Response
from flask_cors import CORS
from flask_pymongo import PyMongo
import bcrypt
import uuid
import os
import datetime
import jwt
import json
from bson import json_util

import RSA

app = Flask(__name__)
CORS(app) 

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

secretKey='keyjwt'
# img = Image.open("static/upload/52785b27-aafc-4ae8-a5bf-f590664b4766.png")
# print(img)
# new_img = img.filter(ImageFilter.GaussianBlur(radius=5))
# new_img.show()


mongodb_client = PyMongo(app, uri="mongodb+srv://phamnguyet:nguyetchuot.12@cluster0.w4fcj.mongodb.net/test")
db = mongodb_client.db

@app.route('/api/upload', methods=['POST'])
def upload():
    # file_to_upload = request.files['image']
    # extension = os.path.splitext(file_to_upload.filename)[1]
    # f_name = str(uuid.uuid4()) + extension
    # file_to_upload.save(os.path.join('static/upload', f_name))
    # return jsonify({'success': True})

    rawImage=request.json['image']
    width=request.json['width']
    height=request.json['height']
    name=request.json['name']
    key_encrypt=request.json['key']
    token=request.headers['Authorization'].split(' ')[1]
    username = jwt.decode(token,secretKey, algorithms=['HS256'])
    user = db.user.find_one({"username": username['username']})
    AES_KEY=db.aes_key.find_one({"key_encrypt":key_encrypt})
    if user:
        db.image.insert_one({'ciphertext': rawImage,
                            'user':user['_id'],
                            'name': name,
                            'width': width,
                            'height':height,
                            'key': AES_KEY['key'],
                            'shareId':[],
                            'createdAt': datetime.datetime.now()
                            })
        db.aes_key.delete_one({"key_encrypt":key_encrypt})
        return jsonify(success=True)
    else:
        return jsonify(success=False,message='User không tồn tại')

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
    encoded_jwt = jwt.encode({'username': username},secretKey, algorithm='HS256')
    user = db.user.find_one({"username": username})
    if user:
        if bcrypt.checkpw(password.encode(), user['password']):
            return jsonify(success=True,token=encoded_jwt)
        return jsonify(success=False, message='Mật khẩu không chính xác')
    return jsonify(success=False, message='Tài khoản không tồn tại')

@app.route('/api/my-image', methods=['GET'])
def get_image():
    token=request.headers['Authorization'].split(' ')[1]
    username = jwt.decode(token,secretKey, algorithms=['HS256'])
    user = db.user.find_one({"username": username['username']})
    if user:
        all_image=db.image.find({"user":user['_id']})
        data=json_util.dumps(all_image)
        return Response(data,mimetype='application/json')
    else:
        return jsonify(success=False,message='User không tồn tại')

@app.route('/api/rsa', methods=['POST'])
def getRSA():
    n = request.json['n']
    e = request.json['e']
    print(n,e)
    AES_KEY=str(uuid.uuid1()).split('-')[0] +'theone'
    print(AES_KEY)
    e=int(str(e),10)
    n=int(str(n),10)
    AES_KEY_ENCRYPT=RSA.encryption(AES_KEY,e,n)
    print(AES_KEY_ENCRYPT)
    print(type(AES_KEY_ENCRYPT))
    db.aes_key.insert_one({
        'key':str(AES_KEY),
        'key_encrypt':str(AES_KEY_ENCRYPT)
    })
    return jsonify(success=True, AES_KEY=str(AES_KEY_ENCRYPT))

@app.route('/api/test', methods=['GET'])
def test():
    print('vo day')
    return jsonify(success=False, message='Tài khoản không tồn tại')


if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
