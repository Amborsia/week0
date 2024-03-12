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