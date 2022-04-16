from flask_restx import Namespace, Resource
from flask import render_template, redirect, url_for, make_response, request, session, flash, jsonify
from controll.image_model import ImageTable
from PIL import Image
import io
import torch
import io
import argparse
from controll.food_model import food_model
from controll.today_cal import today_cal
import numpy as np
import pandas as pd


status = Namespace('status')


@ status.route('/')
class Register(Resource):
    def get(self):

        return make_response(render_template('status.html'))

    def post(self):

        # parser = argparse.ArgumentParser(
        #     description="Flask app exposing yolov5 models")
        # parser.add_argument("--port", default=5000,
        #                     type=int, help="port number")
        # args = parser.parse_args()

        model = torch.hub.load(
            "./yolov5_models/yolov5", "custom", path='./yolov5_models/test.pt', source='local', force_reload=True)
        df = pd.read_excel(
            './yolov5_models/test.xlsx', engine='openpyxl')
        model.names = df['status2'].to_list()
        # print(model.names)

        # model.names = ['쌀밥'] * 400
        # force_reload = recache latest code

        model.eval()

        d = request.files['image']

        # data = request.form['user_email']
        # print('sdjklsjdfkljsdfsldf', data)
        # user_email = list(filter(lambda x: 'user_email' in x,
        #                          data.split(';')))[0].split('=')[1]

        img_bytes = d.read()

        img = Image.open(io.BytesIO(img_bytes))
        results = model(img, size=640)
        results.render()  # updates results.imgs with boxes and labels
        for img in results.imgs:
            img_base64 = Image.fromarray(img)
            filename = d.filename.split('.jpg')
            img_base64.save(
                f"./static/{filename[0]}2.jpeg", format="JPEG")

        data = results.pandas().xyxy[0].to_json(orient="records")
        cal = results.pandas().xyxy[0]['class'].values
        name = results.pandas().xyxy[0]['name'].values

        # ImageTable.add_image(
        #     user_email, f'{filename[0]}.jpeg', cal, name)
        # result = ImageTable.get_image(user_email)[-1].image
        # result2 = ImageTable.get_image(user_email)[-1].cal
        # result3 = food_model.get()
        # abc = result2[1:-1]
        # abc = abc.split()
        # temp = []
        # for i in abc:
        #     temp.append(result3[int(i)])

        # return jsonify({'result': result, 'result2': result2, 'result3': temp})
        return jsonify({'result': filename[0]})
