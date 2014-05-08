from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Cloud(db.Model):
    __tablename__ = 'cloud'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False, default='', server_default='')

    def __repr__(self):
        return '<Cloud {}: {}>'.format(self.id, self.name)


class Machine(db.Model):
    __tablename__ = 'machine'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, default='', server_default='')
    cloud_id = db.Column(db.Integer, db.ForeignKey('cloud.id'), nullable=False)
    cloud = db.relationship(Cloud)

    def __repr__(self):
        return '<Machine {}: {}>'.format(self.id, self.name)
