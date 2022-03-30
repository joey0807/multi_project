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
@app.route('/check2', methods=['GET', 'POST'])
def check2():
    Email = request.form.get('Email')
    name = request.form.get('name')
    pw = request.form.get('pw')
    pw2 = request.form.get('pw2')

    data = User.get(Email)

    if Email == '' or name == '' or pw == '' or pw2 == '':
       flash('입력되지 않은 칸이 있습니다')
       return render_template('register.html')

    if pw != pw2:
        flash('비밀번호가 일치하지 않습니다')
        return render_template('register.html')


    if data :
       flash('사용할 수 없는 Email입니다')
       return render_template('register.html')
    else :
        User.create(Email, name, pw)
        flash('회원가입이 완료되었습니다')
        return render_template('register.html')



# 로그인
@app.route('/login')
def login():
    if session.get('Email', None) is not None:

        return redirect(url_for('mainpage'))
    else:
        return render_template('login.html')


# 로그인 체크
@app.route('/check', methods=['POST'])
def check():   
    Email = request.form.get('Email')
    pw = request.form.get('pw')
    data = User.get(Email)
    # print(data)

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
        return redirect(url_for('login'))
    else:
        flash('로그인을 해야 합니다')
        return redirect(url_for('login'))



# 메인페이지
@app.route('/mainpage')
def mainpage():
    if session.get('Email', None) is not None: #로그인이 돼야
        
        data = pd.DataFrame(Info.find(session['Email']))

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
    else: #로그인이 안되면 mainpage로 못넘어감
        flash('로그인을 해야 합니다')
        return render_template('login.html')

    

# 사용자정보 
@app.route('/info')
def info():
    if session.get('Email', None) is not None: #로그인이 돼야
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
    if 'Email' in session:
        return render_template("graph.html", width=800, height=600)



# 몸무게 변화량 시각화 그래프
@app.route('/fig')
def fig():

    plt.figure(figsize=(6, 7))

    data = pd.DataFrame(Info.find(session['Email']))
    #data.set_index('datetime', inplace=True)
    #print(data)


    data.set_index(data[10], inplace=True)

    plt.title('weight graph')
    plt.xticks(rotation=30)
    plt.plot(data[4])

    img = BytesIO()
    plt.savefig(img, format='png', dpi=300)
    img.seek(0)

    return send_file(img, mimetype='image/png')

#권장섭취량 시각화
# @app.route('/fig2', methods=['GET','POST'])
# def fig2():

#     data = pd.DataFrame(Info.find(session['Email']))

#     sex = data.iloc[-1][3]
#     age = data.iloc[-1][2]

#     print(sex, age)

#     data2 = pd.DataFrame(Info.find2(sex,age))

#     value1 = data2[2].to_string(index=False)
#     value2 = data2[3].to_string(index=False)
#     value3 = data2[4].to_string(index=False)
#     value4 = data2[5].to_string(index=False)
#     value5 = data2[6].to_string(index=False)
#     value6 = data2[7].to_string(index=False)
#     value7 = data2[8].to_string(index=False)
#     value8 = data2[9].to_string(index=False)
#     value9 = data2[10].to_string(index=False)
#     value10 = data2[11].to_string(index=False)
#     value11 = data2[12].to_string(index=False)
#     value12 = data2[13].to_string(index=False)
#     value13 = data2[14].to_string(index=False)
#     value14 = data2[15].to_string(index=False)
#     #print(value1)

#     return render_template('mainpage.html', value1 = value1,value2 = value2,value3 = value3,value4 = value4,value5 = value5,value6 = value6,value7 = value7,value8 = value8,value9 = value9,value10 = value10,value11 = value11,value12 = value12,value13 = value13,value14 = value14)
#     #return "<h3>"+value1+"</h3>" 

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(host="0.0.0.0", port="2888", debug=True)
