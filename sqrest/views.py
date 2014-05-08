from flask import Flask, jsonify
from flask.views import MethodView
from flask.ext.sqlalchemy import SQLAlchemy
from sqrest import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


def register(cls):
    model_name = cls.__name__
    service = type('{}RestService'.format(model_name), (Service,), {'__model__': cls})
    app.add_url_rule('/{}'.format(model_name.lower()), model_name, service.as_view(model_name))

class Service(MethodView):
    __model__ = None

    def get(self, primary_key=None):
        return jsonify([x.as_dict() for x in self.__model__.query.all()])

register(models.Machine)

if __name__ == '__main__':
    app.run(debug=True)