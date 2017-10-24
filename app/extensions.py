##############
# SQLAlchemy #
##############
# Prepare the application to work with SQLAlchemy.
# "db" object is not bound to the app object without setting up an application context
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class BaseDB(db.Model):
    __abstract__ = True
    
    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

##############
# Flask-Mail #
##############
# email are managed through a Mail instance
from flask_mail import Mail
mail = Mail()
