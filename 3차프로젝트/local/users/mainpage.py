from flask_restx import Namespace, Resource
from flask import render_template, redirect, url_for, make_response, request, session, flash, send_file
from controll.cal_model import Calorie_model
from controll.user_info_model import user_info_table
from controll.image_model import ImageTable
from controll.today_cal import today_cal
import numpy as np
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import matplotlib.font_manager as fm


mainpage = Namespace('mainpage')


@mainpage.route('/')
class Mainpage(Resource):
    def get(self):
        print(session)
        if 'token' in session:
            try:
                user_data = request.cookies.get('user_email').split('%40')
                user_email = user_data[0] + '@' + user_data[1]
                print(user_email)
                user = user_info_table.search(user_email)
                sex = user[-1].sex
                age = user[-1].age
                result = Calorie_model.get(sex, age)
                temp = today_cal.get_cal(user_email)

                efg = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                for i in temp:

                    abc = np.array(
                        [i.number1, i.number2, i.number3, i.number4, i.number5, i.number6, i.number7, i.number8, i.number9, i.number10, i.number11, i.number12,
                         i.number13, i.number14])

                    efg += abc

            except:
                result = [0] * 20
                efg = [0] * 20

            return make_response(render_template('mainpage.html', cal_data=result, today_data=efg))
        else:
            return make_response(render_template('login.html'))


@mainpage.route('/login')
class Login(Resource):
    def get(self):
        if 'token' in session:
            return make_response(redirect(url_for('mainpage_mainpage')))
        else:
            return make_response(render_template('login.html'))


@ mainpage.route('/register')
class Register(Resource):
    def get(self):
        if 'token' in session:
            session.pop('token')
        return make_response(render_template('register.html'))


@ mainpage.route('/logout')
class Register(Resource):
    def get(self):
        if 'token' in session:
            session.pop('token')
            return make_response(redirect(url_for('mainpage_login')))
        else:
            return make_response(redirect(url_for('mainpage_login')))


@ mainpage.route('/info')
class Register(Resource):
    def get(self):
        if 'token' in session:
            try:
                user_data = request.cookies.get('user_email').split('%40')
                user_email = user_data[0] + '@' + user_data[1]
                user = user_info_table.search(user_email)[-1]
            except:
                user = None
            return make_response(render_template('info.html', user=user))
        else:
            return make_response(redirect(url_for('mainpage_login')))


@ mainpage.route('/fig')
class Register(Resource):
    def get(self):
        # if 'token' in session:
        plt.figure(figsize=(6, 7))
        user_data = request.cookies.get('user_email').split('%40')
        user_email = user_data[0] + '@' + user_data[1]
        user = user_info_table.search(user_email)

        weight = []
        datetime = []

        print('user[1].weight : ', user[1].weight)
        print("user[1].datetime.strftime('%Y-%m-%d') : ",
              user[1].datetime.strftime('%Y-%m-%d'))
        #user.datetime = DateTime.Parse(myStringDate)

        for x in range(len(user)):
            weight.append(user[x].weight)
            datetime.append(str(user[x].datetime.strftime('%Y-%m-%d')))

        print('weight :', weight)
        print('datetime : ', datetime)

        #plt.rcParams['axes.facecolor'] = 'y'
        BMJUA = fm.FontProperties(
            fname='/home/ubuntu/anaconda3/envs/python3/fonts/BMJUA_ttf.ttf')

        plt.plot(datetime, weight, color='#375bfa')
        plt.plot(datetime, weight, 'go', color='#375bfa')
        plt.title('몸무게 변화', fontsize=30, fontproperties=BMJUA)
        plt.xticks(rotation=30)
        img = BytesIO()
        plt.savefig(img, format='png', dpi=300)
        img.seek(0)

        return send_file(img, mimetype='image/png')


@ mainpage.route('/fig2')
class Register(Resource):
    def get(self):

        plt.figure(figsize=(6, 7))
        user_data = request.cookies.get('user_email').split('%40')
        user_email = user_data[0] + '@' + user_data[1]
        user = today_cal.search(user_email)

        #print('user_email :', user_email)
        #print('user : ',user)
        # print('user[1].number1 : ',user[1].number1)
        # print('user[1] : ',user[1])
        week = []

        for x in range(len(user)):
            user_calory = user[x].number1  # 칼로리
            # user_tansu = user[x].number2 #탄수화물
            # user_jibang = user[x].number4 #지방
            # user_danbak = user[x].number5 #단백질
            datetime = user[x].datetime  # 시간

            day = [user_calory, datetime]

            week.append(list(day))  # 계정에 맞는 칼로리와 탄단지와 시간 정보

        print('week : ', week)

        df = pd.DataFrame(week)
        print(df)
        #print('len(df) :',len(df))
        # print(df.loc[0],df.loc[4])
        #df2 = pd.DataFrame(df.groupby([4]).sum())
        # print(df.groupby([4]).sum())
        # print(df2)
        # print(df2[2])

        df[2] = df.groupby(by=[1])[0].transform(lambda x: x.cumsum())
        print(df)

        ax = plt.subplot()
        ax.bar(df[1], df[2], color='#375bfa')
        ax.xaxis_date()
        # w = 0.15
        # nrow = df.shape[0]
        # idx = np.arange(nrow)
        # for x in ax.patches:
        # height = x.get_height()
        # ax.text(x.get_x() + x.get_width()/2., height+3, height, ha='center', size=10)
        # plt.bar(idx, df[2], width = w)
        # plt.xticks(idx, df[1].dt.date, rotation = 30)
        BMJUA = fm.FontProperties(
            fname='/home/ubuntu/anaconda3/envs/python3/fonts/BMJUA_ttf.ttf')
        plt.title('칼로리 변화', fontsize=30, fontproperties=BMJUA)
        plt.xticks(rotation=30)

        img = BytesIO()
        plt.savefig(img, format='png', dpi=300)
        img.seek(0)
        return send_file(img, mimetype='image/png')


@ mainpage.route('/fig3')
class Register(Resource):
    def get(self):

        plt.figure(figsize=(6, 7))
        user_data = request.cookies.get('user_email').split('%40')
        user_email = user_data[0] + '@' + user_data[1]
        user = today_cal.search(user_email)

        week = []

        for x in range(len(user)):
            # user_calory = user[x].number1 #칼로리
            user_tansu = user[x].number2  # 탄수화물
            user_jibang = user[x].number4  # 지방
            user_danbak = user[x].number5  # 단백질
            datetime = user[x].datetime  # 시간

            day = [user_tansu, user_jibang, user_danbak, datetime]

            week.append(list(day))  # 계정에 맞는 칼로리와 탄단지와 시간

        print('week : ', week)

        df = pd.DataFrame(week)
        # print(df)

        df[4] = df.groupby(by=[3])[0].transform(lambda x: x.cumsum())
        df[5] = df.groupby(by=[3])[1].transform(lambda x: x.cumsum())
        df[6] = df.groupby(by=[3])[2].transform(lambda x: x.cumsum())
        # print(df)
        # print(df.index.is_unique)
        # print(df[3][:])
        # print(df.groupby(level=0).last())
        ax = plt.subplot()

        ax.xaxis_date()

        BMJUA = fm.FontProperties(
            fname='/home/ubuntu/anaconda3/envs/python3/fonts/BMJUA_ttf.ttf')
        plt.title('영양분 변화', fontsize=30, fontproperties=BMJUA)

        w = 0.3
        idx = date2num(df[3])

        test1 = ax.bar(idx - w, df[4], width=w, color='g')
        test2 = ax.bar(idx, df[5], width=w, color='orange')
        test3 = ax.bar(idx + w, df[6], width=w, color='gold')
        ax.xaxis_date()
        plt.xticks(rotation=30)

        # for x in ax.patches:
        # height = x.get_height()
        # ax.text(x.get_x() + x.get_width()/2., height+3, height, ha='center', size=10)

        legend = ax.legend((test1, test2, test3),
                           ('Carbonhydrate', 'Protein', 'Fat'))
        frame = legend.get_frame()
        frame.set_alpha(1)
        frame.set_facecolor('none')  # legend

        img = BytesIO()
        plt.savefig(img, format='png', dpi=300)
        img.seek(0)
        return send_file(img, mimetype='image/png')


@ mainpage.route('/uploader')
class Register(Resource):
    def post(self):

        f = request.files['file']
        print('hi')

        f.save('../static/' + f.filename)

        return 'file uploaded successfully'


@ mainpage.route('/test')
class Register(Resource):
    def get(self):
        token = request.cookies.get('token')

        session['token'] = token

        return make_response(redirect(url_for('mainpage_login')))

@ mainpage.route('/secret') 
class Register(Resource):    
    def get(self):
       return make_response(render_template('secret.html'))   
