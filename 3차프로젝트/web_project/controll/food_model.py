from marshmallow import Schema, fields, validate
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import bcrypt
import datetime
from flask_login import UserMixin
import pymysql
import pandas as pd

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


class food_model(UserMixin):
    def __init__(self, Email, name, pw):
        self.Email = Email
        self.name = name
        self.pw = pw

    def get_Email(self):
        return str(self.Email)

    def get_pw(self):
        return str(self.pw)

    @staticmethod
    def get():
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = f'select * from 영양데이터DB ;'

        result = db_cursor.execute(sql)
        print(result)

        user = db_cursor.fetchall()
        if not user:
            return None

        return user
