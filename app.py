
#bcrypt 사용자의 비밀번호 보관에 특화되어 있는 것 빠르게, 보안도 신경썼다는 티를 내면서 구현하기 위해서는 bcrypt를 사용, 만약 보안에 좀 더 민감하다면 scrypt
# 현시점 비밀번호 저장의 끝판왕은 Argon2id
from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://ghdrms1220:test@cluster0.u8jwhhi.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbjungle

from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# 로그인 html
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/write')
def write():
    return render_template('write.html')

@app.route('/mypage')
def mypage():
    return render_template('mypage.html')