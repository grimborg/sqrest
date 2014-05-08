import urlparse

from flask import Flask, jsonify, request, url_for
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
    __model_name__ = None

    def get(self, primary_key=None):
        r = {self.__model_name__ + 's': [map(self._model_to_dict, self.__model__.query)]}
        print url_for(self.__model_name__)
        return jsonify(**r)

    def post(self):
        obj = self.__model__(**request.json)
        db.session.add(obj)
        db.session.commit()
        r = {self.__model_name__: self._model_to_dict(obj)}
        return jsonify(**r)

    def _model_to_dict(self, obj):
        r = dict()
        for c in obj.__table__.columns:
            r[c.name] = getattr(obj, c.name)
        r['url'] = urlparse.urljoin(url_for(self.__model_name__, _external=True), str(obj.id))
        return r

register(models.Machine)

if __name__ == '__main__':
    app.run(debug=True)
