from pymongo import MongoClient
import certifi
import jwt
import datetime
import bcrypt
import os
import json
import base64
from flask import Flask, render_template, jsonify, request, make_response
from flask_cors import CORS
ca = certifi.where()
client = MongoClient('mongodb+srv://ghdrms1220:test@cluster0.u8jwhhi.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbjungle

app = Flask(__name__)
CORS(app)
SECRET_KEY = 'SWAPJUNGLE'
# 이미지 올릴 때 가능한 포맷형태
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

@app.route('/')
def home():
    return render_template('index.html', image_file='img/logo.png')
# 로그인 html
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/register')
def register():
    return render_template('signup.html')

# EditPost - 완료
@app.route('/edit-post/<dates>')
def edit_post(dates):
    user = db.write.find_one({"date":dates})
    post = {
        'title': user['title'],
        'content': user['content'],
        'date': user['date'],
        'image_url': user['image_url'],
        'status': True
    }
    return render_template('editPost.html', post=post)

# 전체 글 목록 보여주기
@app.route('/posts')
def main():
    
    token = request.cookies.get('token')
    print(token)
    try:
        #token을 시크릿키로 디코딩
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        print(payload)
        #payload안에 아이디값이 들어있기때문에 이 아이디 값으로 유저정보를 찾게됨
        all_users = list(db.write.find({'status':True},{'_id':False}).sort({"_id":-1}))
        return render_template('postList.html', posts=all_users)
    # token이 만료되었을 시
    except jwt.ExpiredSignatureError:
        print('expired1')
        return jsonify({'result':'fail1', 'msg' : '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        print('expired2')
        return jsonify({'result':'fail2', 'msg' : '로그인 정보가 존재하지 않습니다.'})
    
@app.route('/posts/create')
def write():
    return render_template('postCreate.html')
#내 글 목록 포스트 보여주는것 - 완료
@app.route('/my-posts')
def my_posts():
    #토큰을 통해서 누구인지 찾아야함
    token = request.cookies.get('token')
    try:
        #token을 시크릿키로 디코딩
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        
        #payload안에 아이디값이 들어있기때문에 이 아이디 값으로 유저정보를 찾게됨
        all_users = list(db.write.find({"id":payload['id']}))
        
        return render_template('myPosts.html', posts=all_users)
    # token이 만료되었을 시
    except jwt.ExpiredSignatureError:
        return jsonify({'result':'fail1', 'msg' : '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result':'fail2', 'msg' : '로그인 정보가 존재하지 않습니다.'})
    
# 로그인 기능 구현 - 완료
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    id_receive = data.get('id_give')
    pw_receive = data.get('pw_give')
    #입력된 비밀번호를 바이트 코드로 변환
    pw_value = pw_receive.encode('UTF-8')
    # id, 암호화된 pw를 가지고 해당 유저를 찾음
    # 이 값을 바탕으로 입력된 비밀번호를 찾아서 바이트 코드로 변환
    origin_value = db.jungle.find_one({'id':id_receive})
    #비교를 진행하여 다른 True가 나온다면 jwt생성 후 전달
    print(origin_value)
    if origin_value is not None:
        result = bcrypt.checkpw(pw_value,origin_value['pw'])
        if result is True:
            #jwt 토큰 생성 페이로드는 남에게 보여져도 상관없는 데이터만 넣어야함
            payload = {
                # 토큰 발급자
                "iss" : "swapjungle",
                # 토큰 유효기간 설정
                'exp' : datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=100),
                'id' : id_receive
            }
            
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            resp = jsonify({'result' : 'success', 'token' : token})
            resp.set_cookie('userID', id_receive)
            resp.set_cookie('token', token)
            
            
            return resp
            
        else:
            # error 보내기
            return jsonify({'result' : 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
    else:
        return jsonify({'result' : 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# 회원가입 - 완료
@app.route('/api/signup', methods=['POST'])
def api_register():
    data = request.get_json()
    id_receive = data.get('id_give')
    print(id_receive)
    number_receive = data.get('num_give')
    pw_receive = data.get('pw_give')
    pw_plain = pw_receive.encode('UTF-8')
    # 기존 저장된 값을 연산을 위해서 hex에서 바이트로 변환시켜서 DB에 저장하게됨
    pw_text = bcrypt.hashpw(pw_plain, bcrypt.gensalt()).hex()
    origin_pw = bytes.fromhex(pw_text)
    #이미 존재하는가를 확인
    result_id = db.jungle.find_one({'id' : id_receive})
    result_num = db.jungle.find_one({'num' : number_receive})
    if result_id is not None:
        return jsonify({'result' : 'fail', 'msg' : '이미 존재하는 아이디입니다'})
    if result_num is not None:
        return jsonify({'result' : 'fail', 'msg' : '이미 존재하는 번호입니다'})
    else:
        db.jungle.insert_one({'id': id_receive, 'num' : number_receive, 'pw' : origin_pw})
        return jsonify({'result' : 'success'})
    

# 보안을 위해서 만드는 로그인한 사용자만 통과할 수 있는 api 추후에 작업해봐야함 https://duckgugong.tistory.com/274
# @app.route('/api/auth', methods=['GET'])
# def check_auth():
#     token_receive = request.cookies.get('token')
#     try:
#         #token을 시크릿키로 디코딩
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['H256'])
#         #payload안에 아이디값이 들어있기때문에 이 아이디 값으로 유저정보를 찾게됨
#         userinfo = db.jungle.find_one({'id': payload['id'], '_id':0})
#         return jsonify({'result':'success'})
#     # token이 만료되었을 시
#     except jwt.ExpiredSignatureError:
#         return jsonify({'result':'fail1', 'msg' : '로그인 시간이 만료되었습니다.'})
#     except jwt.exceptions.DecodeError:
#         return jsonify({'result':'fail2', 'msg' : '로그인 정보가 존재하지 않습니다.'})
    

# 사진 및 글 업로드 - 완료
@app.route('/write', methods=['POST'])
def save_pic():
    #토큰을 통해서 아이디 구해오기
    #일반 글쓰기
    title_receive = request.form.get('post_title')
    content_receive = request.form.get('post_description')
    #파일 저장을 위한 부분
    file = request.files["savefile"]
    #파일 확장자 작업
    extension = file.filename.split('.')[-1]
    extension_check = extension in ALLOWED_EXTENSIONS
    #만약 확장자가 jpg, png, jpeg가 아니라면 에러발생
    if extension_check is False:
        return jsonify({'result' : 'fail', 'msg':'파일 형식이 다릅니다'})
    else:
        #파일 이름 지정
        today = datetime.datetime.now(datetime.timezone.utc)
        current_time = today.strftime('%Y-%m-%d-%H-%M-%S')
        filename = f'file-{current_time}'
        save_to = f'static/img/{filename}.{extension}'
        image_url = f'static/img/{filename}.{extension}'
        
        token = request.cookies.get('token')
        # 쿠키를 들고오기 위해서 request값을 사용 하지만 '-'이 토큰에 존재하기 때문에 payload로는 읽을 수 없었음
        # 따라서 base64로 인코딩해서 작업을 시작함 밑에 줄들로 디코드를 하면 payload값이 나오게 됨
        # 이상하게 다시 decode가 잘되기 때문에 이 부분은 없애 놓습니다,
        
        # parts = token.split(".")
        # if len(parts) != 3:
        #     raise Exception("Incorrect id token format")
        # payload = parts[1]
        # padded = payload + "=" * (4 - len(payload) % 4)
        # decoded = base64.b64decode(padded).decode('utf-8')
        
        # # 문제는 decoded된 값이 json형식으로 지정되어있기 때문에 우리는 json으로 다시 로드해서 그 안에 값을 지정시켜야함
        # data = json.loads(decoded)['id']
        
        #print(json.loads(decoded))
        
        # if json.loads(decoded)['exp'] < datetime.datetime.now(datetime.timezone.utc)*1000:
            
        #     print('fail1')
        #     return jsonify({'result':'fail1','msg' : '로그인 시간이 만료되었습니다.'})
        
        if token is None: # 토큰이 존재하지 않는다면
            print('fail3')
            return jsonify({'result':'fail3', 'msg' : '로그인 정보가 존재하지 않습니다.'})
        try:
            #token을 시크릿키로 디코딩
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            
            #payload안에 아이디값이 들어있기때문에 이 아이디 값으로 유저정보를 찾게됨
            userinfo = db.jungle.find_one({'id': payload['id']})
            print(userinfo)
            #실제 유저가 맞는지를 토큰과 함께 비교하면서 지정
            if userinfo is None:
                print('fail4')
                return jsonify({'result':'fail4', 'msg' : '올바른 유저가 아닙니다.'})
            else:
                file.save(save_to)
                
                #print(payload)
                my_num = userinfo['num']
                doc = {
                    'title' : title_receive,
                    'content' : content_receive,
                    'file' : f'{filename}.{extension}',
                    'date' : current_time,
                    'image_url' : image_url,
                    'id' : payload['id'],
                    'num' : my_num,
                    #status true 활성화상태
                    'status': True
                    # ?? postnum이 필요할까?
                }
                db.write.insert_one(doc)
                return jsonify({'result' : 'success','msg':'저장완료'})
        # token이 만료되었을 시
        except jwt.ExpiredSignatureError:
            print('fail1')
            return jsonify({'result':'fail1', 'msg' : '로그인 시간이 만료되었습니다.'})
        except jwt.exceptions.DecodeError:
            print('fail2')
            return jsonify({'result':'fail2', 'msg' : '로그인 정보가 존재하지 않습니다.'})

#수정 글쓰기
@app.route('/edit/<date>', methods = ['GET','POST'])
def edit_value(date):
    token = request.cookies.get('token')

    if token is None: # 토큰이 존재하지 않는다면
        print('fail3')
        return jsonify({'result':'fail3', 'msg' : '로그인 정보가 존재하지 않습니다.'})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        print('fail1')
        return jsonify({'result':'fail1', 'msg' : '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        print('fail2')
        return jsonify({'result':'fail2', 'msg' : '로그인 정보가 존재하지 않습니다.'})
    user = db.write.find_one({'date':date})
    if user['id'] != payload['id']:
        return jsonify({'result':'fail5', 'msg' : '올바른 유저가 아닙니다.'})
    userinfo = db.jungle.find_one({'id': payload['id']})
    if userinfo is None:
        print('fail4')
        return jsonify({'result':'fail4', 'msg' : '올바른 유저가 아닙니다.'})
    
    if request.method == 'GET':
        post = db.write.find_one({'date': date})
        if not post:
            return jsonify({'result': 'fail5', 'msg': '올바른 파일이 아닙니다.'}), 404
        return render_template('editPost.html', post=post)
    
    elif request.method == 'POST':
    
        title_receive = request.form.get('post_title')
        content_receive = request.form.get('post_description')
        today = datetime.datetime.now(datetime.timezone.utc)
        current_time = today.strftime('%Y-%m-%d-%H-%M-%S')
        #파일 저장을 위한 부분
        file = request.files["savefile"]
        
        if file.filename == '':
            db.write.update_one({'date':date},{'$set':{'title':title_receive,'content':content_receive}})
            return jsonify({'result' : 'success','msg':'수정'})
        else:
        #파일 확장자 작업
            extension = file.filename.split('.')[-1]
            extension_check = extension in ALLOWED_EXTENSIONS
            #만약 확장자가 jpg, png, jpeg가 아니라면 에러발생
            if extension_check is False:
                return jsonify({'result' : 'fail', 'msg':'파일 형식이 다릅니다'})
        
        #파일 이름 지정
            url = db.write.find_one({'date':date})
            if os.path.isfile(url['image_url']):
                os.remove(url['image_url'])
            filename = f'file-{current_time}'
            save_to = f'static/img/{filename}.{extension}'
            image_url = f'static/img/{filename}.{extension}'
            file.save(save_to)
            check_date = db.write.find_one({'date':date})
            #date값이 없다면 올바른 파일이 아님을 이야기
            if check_date is None:
                print('fail5')
                return jsonify({'result':'fail5', 'msg' : '올바른 파일이 아닙니다.'})
            else:
                db.write.update_one({'date':date},{'$set':{'title':title_receive,'content':content_receive,'file':f'{filename}.{extension}','date':current_time,'image_url':image_url}})
            
            return jsonify({'result' : 'success','msg':'수정'})
        
#내글목록 포스트
# @app.route('/api/myposts', methods=['GET'])
# def post():
#     #이부분의 파일을 나중에는 아이디값으로 변경해야함
#     my_id = request.cookies.get('id')
#     my_post = list(db.write.find({'id':my_id},{'_id':False}))
#     return jsonify({'result':'success', 'post':my_post})

#내글목록 완료 버튼 - 완료
@app.route('/posts/complete', methods=['POST'])
def post_complete():
    token = request.cookies.get('token')
    
    try:
        #token을 시크릿키로 디코딩
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        
        data = request.get_json()
        date_receive = data.get('date')
        #id_receive = data.get('post_id')
        user = db.write.find_one({'date':date_receive})
        db.write.update_one({'date':date_receive},{'$set':{'status':False}})
        return jsonify({'result':'success'})
    # token이 만료되었을 시
    except jwt.ExpiredSignatureError:
        return jsonify({'result':'fail1', 'msg' : '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result':'fail2', 'msg' : '로그인 정보가 존재하지 않습니다.'})
    

#본문내용 리스트 뿌리기 - 완료
@app.route('/main', methods=['GET'])
def show_main():
    all_users = list(db.write.find({},{'_id':False}))
    return jsonify({'result': 'success', 'value':all_users})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)