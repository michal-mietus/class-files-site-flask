import datetime
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from .app import get_app

db = SQLAlchemy(get_app())
db.init_app(get_app())

bcrypt = Bcrypt(get_app())

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    _password = db.Column(db.Binary(60), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
 
    def __init__(self, email, plaintext_password):
        self.email = email
        self._password = plaintext_password
        self.authenticated = False
 
    @hybrid_property
    def password(self):
        return self._password
 
    @password.setter
    def set_password(self, plaintext_password):
        self._password = bcrypt.generate_password_hash(plaintext_password)
 
    @hybrid_method
    def is_correct_password(self, plaintext_password):
        return bcrypt.check_password_hash(self.password, plaintext_password)


class Image(BaseModel):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key = True)
    section_id = db.Column(db.ForeignKey('sections.id'), nullable=False)
    name = db.Column(db.String)
    extension = db.Column(db.String)
    date = db.Column(db.DateTime)

    def __init__(self, section_id, name, extension, date):
        self.section_id = section_id
        self.name = name
        self.extension = extension
        self.date = date


class Section(BaseModel):
    __tablename__ = 'sections'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name
