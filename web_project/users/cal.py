from matplotlib.font_manager import json_dump
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask import request, jsonify, make_response
from flask_restx import Resource, Api, Namespace, fields
import json
from flask import redirect, url_for, render_template
from controll.cal_model import Calorie_model
from controll.user_info_model import user_info_table
import datetime
import jwt


calorie = Namespace('calorie')

cal_fields = calorie.model('email', {  # Model 객체 생성
    'user_email': fields.String(description='email', required=True)
})


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):

        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    # this will fail on non-encodable values, like other classes
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


@calorie.route('/')
class Calorie(Resource):
    @calorie.expect(cal_fields)
    @calorie.response(200, 'Success', cal_fields)
    def post(self):
        '''기타 정보 추가'''
        data = request.get_json()
        user_email = list(filter(lambda x: 'user_email' in x,
                                 data['user_email'].split(';')))[0].split('=')[1]
        user = user_info_table.search(user_email)
        sex = user[-1].sex
        age = user[-1].age

        result = Calorie_model.get(sex, age)
        print(result)

        return jsonify(result)
