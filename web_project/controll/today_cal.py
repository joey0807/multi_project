from marshmallow import Schema, fields, validate
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import bcrypt
import datetime


today_cal_db = SQLAlchemy()


class today_cal(today_cal_db.Model):
    __tablename__ = 'today_cal'

    ID = today_cal_db.Column(
        today_cal_db.Integer, primary_key=True, autoincrement=True)
    Email = today_cal_db.Column(
        today_cal_db.String(1000, 'utf8mb4_unicode_ci'))
    number1 = today_cal_db.Column(today_cal_db.Integer)
    number2 = today_cal_db.Column(today_cal_db.Integer)
    number3 = today_cal_db.Column(today_cal_db.Integer)
    number4 = today_cal_db.Column(today_cal_db.Integer)
    number5 = today_cal_db.Column(today_cal_db.Integer)
    number6 = today_cal_db.Column(today_cal_db.Integer)
    number7 = today_cal_db.Column(today_cal_db.Integer)
    number8 = today_cal_db.Column(today_cal_db.Integer)
    number9 = today_cal_db.Column(today_cal_db.Integer)
    number10 = today_cal_db.Column(today_cal_db.Integer)
    number11 = today_cal_db.Column(today_cal_db.Integer)
    number12 = today_cal_db.Column(today_cal_db.Integer)
    number13 = today_cal_db.Column(today_cal_db.Integer)
    number14 = today_cal_db.Column(today_cal_db.Integer)
    datetime = today_cal_db.Column(
        today_cal_db.DateTime, default=datetime.datetime.now().strftime('%Y-%m-%d'))

    def __init__(self, Email, number1, number2, number3, number4, number5, number6, number7, number8, number9, number10, number11, number12, number13, number14):
        self.Email = Email
        self.number1 = number1
        self.number2 = number2
        self.number3 = number3
        self.number4 = number4
        self.number5 = number5
        self.number6 = number6
        self.number7 = number7
        self.number8 = number8
        self.number9 = number9
        self.number10 = number10
        self.number11 = number11
        self.number12 = number12
        self.number13 = number13
        self.number14 = number14

    def add_cal(email, number1, number2, number3, number4, number5, number6, number7, number8, number9, number10, number11, number12, number13, number14):
        user = today_cal(email, number1, number2, number3, number4, number5, number6,
                         number7, number8, number9, number10, number11, number12, number13, number14)
        today_cal_db.session.add(user)
        today_cal_db.session.commit()
        return user

    def get_cal(email):
        user = today_cal.query.filter((today_cal.Email == email) & (
            today_cal.datetime == datetime.datetime.now().strftime('%Y-%m-%d'))).all()

        return user

    def del_cal(email):
        user = today_cal.query.filter((today_cal.Email == email) & (
            today_cal.datetime == datetime.datetime.now().strftime('%Y-%m-%d'))).all()[-1]
        today_cal_db.session.delete(user)
        today_cal_db.session.commit()

        return user

    # 정보 조회

    def search(Email):
        user = today_cal.query.filter(
            (today_cal.Email == Email)).all()
        return user
