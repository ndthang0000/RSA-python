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
from bson.objectid import ObjectId

import RSA

app = Flask(__name__)
CORS(app) 

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

secretKey='keyjwt'


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
        return jsonify(success=False,message='User kh??ng t???n t???i')

@app.route('/api/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    name = request.json['name']

    user = db.user.find_one({"username": username})
    hash_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(5))
    if user:
        return jsonify(success=False, message='Username ???? t???n t???i')
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
        return jsonify(success=False, message='M???t kh???u kh??ng ch??nh x??c')
    return jsonify(success=False, message='T??i kho???n kh??ng t???n t???i')

@app.route('/api/my-image', methods=['POST'])
def get_image():
    n = request.json['n']
    e = request.json['e']
    e=int(str(e),10)
    n=int(str(n),10)
    token=request.headers['Authorization'].split(' ')[1]
    username = jwt.decode(token,secretKey, algorithms=['HS256'])
    user = db.user.find_one({"username": username['username']})
    if user:
        all_image=list(db.image.find({"user":user['_id']}))
        for item in all_image:
            item['key']=str(RSA.encryption(item['key'],e,n))
        data=json_util.dumps(all_image)
        return Response(data,mimetype='application/json')
    else:
        return jsonify(success=False,message='User kh??ng t???n t???i')

@app.route('/api/get-share-image', methods=['POST'])
def get_share_image():
    n = request.json['n']
    e = request.json['e']
    e=int(str(e),10)
    n=int(str(n),10)
    token=request.headers['Authorization'].split(' ')[1]
    username = jwt.decode(token,secretKey, algorithms=['HS256'])
    user = db.user.find_one({"username": username['username']})
    if user:
        all_image=list(db.image.find({'shareId':user['_id']}))
        for item in all_image:
            item['key']=str(RSA.encryption(item['key'],e,n))
            item['user']=db.user.find_one({'_id':item['user']})['name']
        data=json_util.dumps(all_image)
        return Response(data,mimetype='application/json')
    else:
        return jsonify(success=False)

@app.route('/api/share-image', methods=['POST'])
def share_image():
    username=request.json['username']
    id=request.json['id']
    user = db.user.find_one({"username": username})
    if user:
        result=db.image.find_one_and_update(
            {'_id': ObjectId(id)},
            { '$push': {'shareId': user['_id']}},
            )
        return jsonify(success=True)
    else:
        return jsonify(success=False,message='Username kh??ng t???n t???i')

@app.route('/api/rsa', methods=['POST'])
def getRSA():
    n = request.json['n']
    e = request.json['e']
    AES_KEY=str(uuid.uuid1()).split('-')[0] +'theone'
    e=int(str(e),10)
    n=int(str(n),10)
    AES_KEY_ENCRYPT=RSA.encryption(AES_KEY,e,n)
    db.aes_key.insert_one({
        'key':str(AES_KEY),
        'key_encrypt':str(AES_KEY_ENCRYPT)
    })
    return jsonify(success=True, AES_KEY=str(AES_KEY_ENCRYPT))

@app.route('/api/test', methods=['GET'])
def test():
    print('vo day')
    return jsonify(success=False, message='T??i kho???n kh??ng t???n t???i')


if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
