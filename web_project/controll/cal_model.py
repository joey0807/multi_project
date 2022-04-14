from marshmallow import Schema, fields, validate
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import bcrypt
import datetime
from flask_login import UserMixin
import pymysql

MYSQL_HOST = '13.112.232.65'
MYSQL_CONN = pymysql.connect(
    host=MYSQL_HOST,
    port=3306,
    user='lab05',
    passwd='lab05',
    db='user',
    charset='utf8'
)


def conn_mysqldb():
    if not MYSQL_CONN.open:
        MYSQL_CONN.ping(reconnect=True)
    return MYSQL_CONN


class Calorie_model(UserMixin):
    def __init__(self, Email, name, pw):
        self.Email = Email
        self.name = name
        self.pw = pw

    def get_Email(self):
        return str(self.Email)

    def get_pw(self):
        return str(self.pw)

    @staticmethod
    def get(sex, age):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = f'select * from 권장섭취량 where sex="{(sex).lower()}" AND age={age};'
        # print(sql)
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            return None

        return user
