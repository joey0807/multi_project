from flask import Flask, jsonify, request, session, render_template, make_response,  flash, redirect, url_for, send_file, make_response
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_cors import CORS
import sys
#sys.path.insert(0, '/home/lab03/kim-project/control')
import flask
import matplotlib
from control.user_mgmt import User
from control.user_mgmt import Image
import os
from datetime import timedelta, datetime
from werkzeug.utils import secure_filename
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from functools import wraps, update_wrapper
from flask_caching import Cache
from control.user_mgmt import Info
import bcrypt
from PIL import Image
import jwt
import torch
import io
import argparse

matplotlib.use('Agg')


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__, static_url_path='/static')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'


@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return make_response(jsonify(success=False), 401)    


@app.route('/')
def home():
    return render_template("login.html")



# 회원가입 
@app.route('/check2')
def check2():
    return render_template('register.html')

# 로그인
@app.route('/login')
def login():
    if session.get('Email', None) is not None:
    #if session.get('user_email', None) is not None:

        return redirect(url_for('mainpage'))
    else:
        return render_template('login.html')


# 로그인 체크
@app.route('/check', methods=['POST'])
def check():   
    Email = request.form.get('Email')
    #Email = request.form.get('user_email')
    pw = request.form.get('pw')
    data = User.get(Email)
    #print('data : ',data)

    # print(pw)

    # return render_template('login.html')
    if data == None: #if data is not None <= 원래 코드 
        flash('회원정보가 없습니다')
        return redirect(url_for('login'))
    else:
        if data.pw == str(pw):
            session['Email'] = str(data.Email)
            session.permanent = True
            flash('로그인 되었습니다')
            return redirect(url_for('mainpage'))
        else:
            flash('비밀번호가 일치하지 않습니다')
            return redirect(url_for('login'))               

    
# 로그아웃
@app.route('/logout')
def logout():
    if session.get('Email', None) is not None:
        session.pop('Email')
    # if session.get('user_email', None) is not None:
    #     session.pop('user_email')
        return redirect(url_for('login'))
    else:
        flash('로그인을 해야 합니다')
        return redirect(url_for('login'))



# 메인페이지
@app.route('/mainpage')
def mainpage():

    #print('세션 :',session)
    # print(request.json['token'])
    # return render_template('mainpage.html')

    #if session.get('Email', None) is not None: #로그인이 돼야
        
    user_email = request.cookies.get('user_email').replace('%40','@')
    data = pd.DataFrame(Info.find(user_email))

    if data.empty:
        return render_template('mainpage.html')
    else:
        sex = data.iloc[-1][3]
        age = data.iloc[-1][2]

        print(sex, age)

        data2 = pd.DataFrame(Info.find2(sex,age))

        value1 = data2[2].to_string(index=False)
        value2 = data2[3].to_string(index=False)
        value3 = data2[4].to_string(index=False)
        value4 = data2[5].to_string(index=False)
        value5 = data2[6].to_string(index=False)
        value6 = data2[7].to_string(index=False)
        value7 = data2[8].to_string(index=False)
        value8 = data2[9].to_string(index=False)
        value9 = data2[10].to_string(index=False)
        value10 = data2[11].to_string(index=False)
        value11 = data2[12].to_string(index=False)
        value12 = data2[13].to_string(index=False)
        value13 = data2[14].to_string(index=False)
        value14 = data2[15].to_string(index=False)

    return render_template('mainpage.html',value1 = value1,value2 = value2,value3 = value3,value4 = value4,value5 = value5,value6 = value6,value7 = value7,value8 = value8,value9 = value9,value10 = value10,value11 = value11,value12 = value12,value13 = value13,value14 = value14)
# else: #로그인이 안되면 mainpage로 못넘어감
    #     flash('로그인을 해야 합니다')
    #     return render_template('login.html')

@app.route('/mealinfo')
def mealinfo():
    return render_template("mealinfo.html") #결과페이지로 넘어갈 수 있음

# 사용자정보 
@app.route('/info')
def info():
    if 'token' in session:
    #if session.get('Email', None) is not None:
    #if session.get('user_email', None) is not None: #로그인이 돼야
        return render_template("info.html") #메인페이지로 넘어갈 수 있음
    else: #로그인이 안되면 mainpage로 못넘어감
        flash('로그인을 해야 합니다')
        return render_template('login.html')         

# 사용자 정보 저장 
@app.route('/userinfo', methods=['GET', 'POST'])
def userinfo():
        Email = request.form.get('Email')
        age = request.form.get('age')
        sex = request.form.get('sex')
        weight = request.form.get('weight')
        height = request.form.get('height')
        exercise = request.form.get('exercise')
        disease = request.form.get('disease')
        drink = request.form.get('drink')
        smoke = request.form.get('smoke')  

        Info.create(Email, age, sex, weight, height, exercise, disease, drink, smoke)
        flash('정보수정이 완료되었습니다')
        return render_template('mainpage.html')

# 리스트 HTML에 이미지를 띄우는 것
@app.route('/list', endpoint='list')
def blog():
    if session['Email'] is not None:
        data = Image.get(session['Email'])
    # if session['user_email'] is not None:
    #     data = Image.get(session['user_email'])
        result = []
        if data is not None:
            for i in data:
                result.append(i[2])

            return render_template('list.html', value=result)
        else:
            return render_template('mainpage.html')




# Id에 맞는 그래프를 가져옴
@app.route('/normal')
def normal():
    if 'token' not in session:
    #if 'Email' in session:
    #if 'user_email' in session:
        return render_template("graph.html", width=800, height=600)



# 몸무게 변화량 시각화 그래프
@app.route('/fig')
def fig():

    plt.figure(figsize=(6, 7))
    user_email = request.cookies.get('user_email').replace('%40','@')
    print(user_email)


    data = pd.DataFrame(Info.find(user_email))
    print(data)
    # print(data)


    data.set_index(data[10], inplace=True)

    plt.title('weight graph')
    plt.xticks(rotation=30)
    plt.plot(data[4])

    img = BytesIO()
    plt.savefig(img, format='png', dpi=300)
    img.seek(0)

    return send_file(img, mimetype='image/png')

@app.route("/detection", methods=["GET", "POST"])
def detection():
    if request.method == "POST":
        if "inputfile" not in request.files:
            return redirect(request.url)
        inputfile = request.files["inputfile"]
        print(inputfile)
        if not inputfile:
            return

        img_bytes = inputfile.read()
        img = Image.open(io.BytesIO(img_bytes))
        results = model(img, size=640)

        results.render()  # updates results.imgs with boxes and labels
        for img in results.imgs:
            img_base64 = Image.fromarray(img)
            img_base64.save("static/detected_imgs/image0.jpg", format="JPEG")

        data = results.pandas().xyxy[0].to_json(orient="records")
        # print(data)
        # {   
        #     filename : ' ',
        #     test : ''
        # }
    # return redirect(url_for("mealinfo"))   
    return render_template("mealinfo.html", data=data)  
    
@app.route('/test')
def test123():
    token = request.cookies.get('token')
    user_email = request.cookies.get('user_email')

    print('이메일 : ',user_email)
    print('토큰 : ',token)
    
    
    try:
        jwt.decode(token, 'secret', algorithms='HS256')
        session['token'] = token
        return redirect(url_for('mainpage'))
    except jwt.ExpiredSignatureError:
        flash('일정 시간이 지나 다시 로그인 해야합니다')
        return redirect(url_for("login"))
    except jwt.exceptions.DecodeError:
        flash('다시 로그인 하세요')
        #print(session)
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()

    model = torch.hub.load(
        "yolov5_models/yolov5", "custom", path='yolov5_models/F2v1.pt', source='local', force_reload=True)
    # model.names =  ['쌀밥', '된장찌개', '족발', '돈가스', '배추김치']
    # force_reload = recache latest code

    model.eval()    

    app.run(host="0.0.0.0", port="2888", debug=True)
