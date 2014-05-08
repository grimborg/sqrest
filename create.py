from sqrest import models
from sqrest.models import *
from sqrest.views import app
with app.app_context():
    db.metadata.create_all(bind=db.engine)

    c = models.Cloud(name='Big Cloud')
    m = models.Machine(name='Big Machine', cloud=c)

    db.session.add(m)
    db.session.commit()
