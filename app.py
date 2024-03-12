# from pymongo import MongoClient
# import certifi
# ca = certifi.where()
# client = MongoClient('mongodb+srv://ghdrms1220:test@cluster0.u8jwhhi.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
# db = client.dbjungle
# from flask import Flask, render_template, jsonify, request
# app = Flask(__name__)
# @app.route('/')
# def home():
#     return render_template('index.html')
# # 로그인 html
# @app.route('/login')
# def login():
#     return render_template('login.html')
# @app.route('/register')
# def register():
#     return render_template('signup.html')
# @app.route('/posts')
# def main():
#     # 몽고디비한테 요청해서 posts 라는 변수를 가져오겠죠
#     # posts = db.posts.find({})
#     posts = [
#         {'title': '첫 번째 게시글', 'image_url': 'https://images.unsplash.com/photo-1708748513828-2227f6d39c04?q=80&w=3540&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 'content': '일반사면을 명하려면 국회의 동의를 얻어야 한다. 혼인과 가족생활은 개인의 존엄과 양성의 평등을 기초로 성립되고 유지되면서도 국가는 보장한다.'},
#         {'title': '두 번째 게시글', 'image_url': 'https://images.unsplash.com/photo-1707667786496-697ebfd08979?q=80&w=1740&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 'content': '두 번째 게시글 내용...'},
#         {'title': '세 번째 게시글', 'image_url': 'https://images.unsplash.com/photo-1707343843437-caacff5cfa74?q=80&w=1675&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 'content': '세 번째 게시글 내용...'},
#     ]
#     return render_template('postList.html', posts=posts)


# @app.route('/myposts')
# def myPosts():
#     return render_template('myPosts.html')
# @app.route('/mypage')
# def mypage():
#     return render_template('mypage.html')

# if __name__ == '__main__':
#     app.run('0.0.0.0', port=5000, debug=True)


from pymongo import MongoClient
import certifi
import hashlib
import jwt
import datetime
import bcrypt
ca = certifi.where()
client = MongoClient('mongodb+srv://ghdrms1220:test@cluster0.u8jwhhi.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbjungle
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)
SECRET_KEY = 'SWAPJUNGLE'
# 이미지 올릴 때 가능한 포맷형태
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/')
def home():
    return render_template('index.html')
# 로그인 html
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/register')
def register():
    return render_template('signup.html')
@app.route('/posts')
def main():
    posts = [
        {'title': '첫 번째 게시글', 'image_url': 'https://images.unsplash.com/photo-1708748513828-2227f6d39c04?q=80&w=3540&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 'content': '일반사면을 명하려면 국회의 동의를 얻어야 한다. 혼인과 가족생활은 개인의 존엄과 양성의 평등을 기초로 성립되고 유지되면서도 국가는 보장한다.'},
        {'title': '두 번째 게시글', 'image_url': 'https://images.unsplash.com/photo-1707667786496-697ebfd08979?q=80&w=1740&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 'content': '두 번째 게시글 내용...'},
        {'title': '세 번째 게시글', 'image_url': 'https://images.unsplash.com/photo-1707343843437-caacff5cfa74?q=80&w=1675&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 'content': '세 번째 게시글 내용...'},
    ]
    return render_template('postList.html', posts=posts)
@app.route('/write')
def write():
    return render_template('write.html')
@app.route('/myposts')
def mypage():
    return render_template('mypage.html')
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    #입력된 비밀번호를 바이트 코드로 변환
    pw_value = pw_receive.encode('UTF-8')
    # id, 암호화된 pw를 가지고 해당 유저를 찾음
    # 이 값을 바탕으로 입력된 비밀번호를 찾아서 바이트 코드로 변환
    origin_value = db.jungle.find_one({'id':id_receive})
    #비교를 진행하여 다른 True가 나온다면 jwt생성 후 전달
    result = bcrypt.checkpw(pw_value,origin_value['pw'])
    if result is True:
        #jwt 토큰 생성 페이로드는 남에게 보여져도 상관없는 데이터만 넣어야함
        payload = {
            # 토큰 발급자
            "iss" : "swapjungle",
            # 토큰 유효기간 설정
            'exp' : datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=100),
            'id' : id_receive
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        # token을 줘야함
        return jsonify({'result' : 'success', 'token' : token})
    else:
        return jsonify({'result' : 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# 회원가입
@app.route('/api/signup', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    number_receive = request.form['num_give']
    pw_receive = request.form['pw_give']
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

@app.route('/api/auth', methods=['GET'])
def check_auth():
    token_receive = request.cookies.get('mytoken')
    try:
        #token을 시크릿키로 디코딩
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['H256'])
        #payload안에 아이디값이 들어있기때문에 이 아이디 값으로 유저정보를 찾게됨
        userinfo = db.jungle.find_one({'id': payload['id'], '_id':0})
        return jsonify({'result':'success'})
    # token이 만료되었을 시
    except jwt.ExpiredSignatureError:
        return jsonify({'result':'fail1', 'msg' : '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result':'fail2', 'msg' : '로그인 정보가 존재하지 않습니다.'})
# 사진 및 글 업로드
@app.route('/write', methods=['POST'])
def save_pic():
    #토큰을 통해서 아이디 구해오기
    token_receive = request.cookies.get('mytoken')
    #일반 글쓰기
    arg = request.args.get('data')
     #title_receive = request.form['title_give']
    #content_receive = request.form['content_give']
    #파일 저장을 위한 부분
    file = request.files["savefile"]
    #파일 확장자 작업
    extension = file.filename.split('.')[-1]
    extension_check = extension in ALLOWED_EXTENSIONS
    #만약 확장자가 jpg, png, jpeg가 아니라면 에러발생
    if extension_check is False:
        return jsonify({'result' : 'fail', 'msg':'파일 형식이 다릅니다'})
    else:
        today = datetime.datetime.now(datetime.timezone.utc)
        current_time = today.strftime('%Y-%m-%d-%H-%M-%S')
        filename = f'file-{current_time}'
        save_to = f'static/{filename}.{extension}'
        file.save(save_to)
        doc = {
        #   'title' : title_receive,
        #  'content' : content_receive,
            'file' : f'{filename}.{extension}',
            'date' : current_time,
            #id값이랑 number값도 함께 넣어놔야함
        #id값을 넣어야 하나???
        }
        db.write.insert_one(doc)
        return jsonify({'result' : 'success','msg':'저장완료'})
#수정 글쓰기
@app.route('/edit', methods = ['GET, POST'])
def edit_value():
    if request.method =='GET' :
        token_receive = request.cookies.get('mytoken')
        try:
            #token을 시크릿키로 디코딩
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['H256'])
            #payload안에 아이디값이 들어있기때문에 이 아이디 값으로 유저정보를 찾게됨
            #내가 쓴 글목록 있는 곳에서 데이터를 들고와야함
            #그러면 제목과 사진 제목이 존재할텐데 그걸 토대로 글 목록에서 find하게되면 글을 찾을 수 있음
            userinfo = db.write.find_one({'id': payload['id'], '_id':0})
            return jsonify({'result':'success'})
        # token이 만료되었을 시
        except jwt.ExpiredSignatureError:
            return jsonify({'result':'fail1', 'msg' : '로그인 시간이 만료되었습니다.'})
        except jwt.exceptions.DecodeError:
            return jsonify({'result':'fail2', 'msg' : '로그인 정보가 존재하지 않습니다.'})
    elif request.method == 'POST' :
        # db에서 찾아서 내용을 바꿔주는 수정값이 필요함
        #파일 저장을 위한 부분
        file = request.files["savefile"]
        #파일 확장자 작업
        extension = file.filename.split('.')[-1]in ALLOWED_EXTENSIONS
        extension_check = extension in ALLOWED_EXTENSIONS
        #os.remove를 사용해서 사진 받아온 값을 삭제해야함
@app.route('/main', methods=['GET'])
def show_main():
    all_users = list(db.write.find({},{'_id':False}))
    return jsonify({'result': 'success', 'value':all_users})
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)