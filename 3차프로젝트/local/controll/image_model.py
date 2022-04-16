from marshmallow import Schema, fields, validate
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import bcrypt
import datetime


image_db = SQLAlchemy()


class ImageTable(image_db.Model):
    __tablename__ = 'Image'

    ID = image_db.Column(
        image_db.Integer, primary_key=True, autoincrement=True)
    Email = image_db.Column(
        image_db.String(1000, 'utf8mb4_unicode_ci'))
    image = image_db.Column(
        image_db.String(2000, 'utf8mb4_unicode_ci'))
    cal = image_db.Column(
        image_db.String(2000, 'utf8mb4_unicode_ci'))
    name = image_db.Column(
        image_db.String(2000, 'utf8mb4_unicode_ci'))
    datetime = image_db.Column(
        image_db.DateTime, default=datetime.datetime.now)

    def __init__(self, Email, image, cal, name):
        self.Email = Email
        self.image = image
        self.cal = cal
        self.name = name

    def add_image(email, image_path, cal, name):
        user = ImageTable(email, image_path, cal, name)
        image_db.session.add(user)
        image_db.session.commit()
        return user

    def get_image(email):
        user = ImageTable.query.filter((ImageTable.Email == email)).all()

        return user
