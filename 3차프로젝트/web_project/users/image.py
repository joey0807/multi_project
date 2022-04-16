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


image = Namespace('image')


@ image.route('/')
class Register(Resource):
    def post(self):

        # parser = argparse.ArgumentParser(
        #     description="Flask app exposing yolov5 models")
        # parser.add_argument("--port", default=8989,
        #                     type=int, help="port number")
        # args = parser.parse_args()

        model = torch.hub.load(
            "./yolov5_models/yolov5", "custom", path='./yolov5_models/AFv1.pt', source='local', force_reload=True)
        # model.names =  ['쌀밥', '된장찌개', '족발', '돈가스', '배추김치']
        # force_reload = recache latest code

        model.eval()

        d = request.files['image']

        data = request.form['user_email']
        user_email = list(filter(lambda x: 'user_email' in x,
                                 data.split(';')))[0].split('=')[1]

        img_bytes = d.read()

        img = Image.open(io.BytesIO(img_bytes))
        results = model(img, size=640)
        results.render()  # updates results.imgs with boxes and labels
        for img in results.imgs:
            img_base64 = Image.fromarray(img)
            filename = d.filename.split('.jpg')
            img_base64.save(
                f"./static/{filename[0]}.jpeg", format="JPEG")

        data = results.pandas().xyxy[0].to_json(orient="records")
        cal = results.pandas().xyxy[0]['class'].values
        name = results.pandas().xyxy[0]['name'].values

        ImageTable.add_image(
            user_email, f'{filename[0]}.jpeg', cal, name)
        result = ImageTable.get_image(user_email)[-1].image
        result2 = ImageTable.get_image(user_email)[-1].cal
        result3 = food_model.get()
        abc = result2[1:-1]
        abc = abc.split()
        temp = []
        for i in abc:
            temp.append(result3[int(i)])

        return make_response(jsonify({'result': result, 'result2': result2, 'result3': temp}))


@ image.route('/')
class Register(Resource):
    def put(self):
        data = request.form['data']
        temp_data = data.split(',')[1:-1]
        print(temp_data)
        user_data = request.form['user_email']
        number = request.form['number']
        number_data = number.split(',')[1:-1]
        data_dict = {}
        for i in range(len(temp_data)):
            if temp_data[i] in data_dict:
                if int(data_dict[temp_data[i]]) >= int(number_data[i]):
                    pass
                else:
                    data_dict[temp_data[i]] = number_data[i]

            else:
                data_dict[temp_data[i]] = number_data[i]

        user_email = list(filter(lambda x: 'user_email' in x,
                                 user_data.split(';')))[0].split('=')[1]
        result2 = ImageTable.get_image(user_email)[-1].cal
        result3 = food_model.get()

        abc = result2[1:-1]
        abc = abc.split()

        temp = {}
        for i in abc:
            temp[result3[int(i)][0]] = result3[int(i)][1:]
            # temp.add(result3[int(i)])

        for idx, val in data_dict.items():
            if int(val) != 1:
                temp2 = []
                for i in range(len(temp[idx])):
                    temp2.append(temp[idx][i] * int(val))
                temp[idx] = temp2
        print(temp)

        sum_cal = np.array([0] * 14)
        for k in data_dict.keys():
            sum_cal += np.array(temp[k][1:]).astype(int)

        today_cal.add_cal(user_email, *sum_cal)


@ image.route('/')
class Register(Resource):
    def delete(self):
        user_data = request.form['user_email']
        user_email = list(filter(lambda x: 'user_email' in x,
                                 user_data.split(';')))[0].split('=')[1]
        today_cal.del_cal(user_email)
