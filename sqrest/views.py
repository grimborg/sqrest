from flask import Flask, jsonify, request
from flask.views import MethodView
from flask.ext.sqlalchemy import SQLAlchemy
from sqrest import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


def register(cls):
    model_name = cls.__name__.lower()
    service = type('{}RestService'.format(model_name), (Service,), {'__model__': cls, '__model_name__': model_name})
    app.add_url_rule('/{}'.format(model_name.lower()), model_name, service.as_view(model_name))


class Service(MethodView):
    __model__ = None

    def get(self, primary_key=None):
        r = {self.__model_name__ + 's': [map(self._serialize, self.__model__.query)]}
        return jsonify(**r)
        #return jsonify(machines=[self._serialize(x) for x in self.__model__.query.all()])

    def post(self):
        obj = self.__model__(**request.json)
        db.session.add(obj)
        db.session.commit()
        r = {self.__model_name__: self._serialize(obj)}
        return jsonify(**r)

    def _serialize(self, obj):
        r = dict()
        for c in obj.__table__.columns:
            r[c.name] = getattr(obj, c.name)
        return r

register(models.Machine)

if __name__ == '__main__':
    app.run(debug=True)
