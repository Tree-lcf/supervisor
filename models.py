from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, *args, **kwargs):
        telephone = kwargs.get('telephone')
        username = kwargs.get('username')
        password = kwargs.get('password')

        self.telephone = telephone
        self.username = username
        self.password = generate_password_hash(password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', backref=db.backref('projects'))


class API(db.Model):
    __tablename__ = 'api'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    module = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    method = db.Column(db.String(100), nullable=False)
    headers = db.Column(db.Text, nullable=False)
    payload = db.Column(db.Text)
    result = db.Column(db.Integer, default=2)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', backref=db.backref('api'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    project = db.relationship('Project', backref=db.backref('api', order_by=create_time.desc()))