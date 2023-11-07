from __future__ import annotations
from flask import current_app
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required
from dotenv import load_dotenv
from colorful.auth.hasher import UpdatedHasher

load_dotenv()
db = SQLAlchemy()
pepper_key = os.getenv('PEPPER_KEY')
password_hasher = UpdatedHasher(pepper_key=pepper_key)

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, nullable=False)
    currentStatusID = db.Column(db.Integer, db.ForeignKey("Status.id"), nullable=True)
    
    # TODO: Add Relationships between tables

    email = db.Column(db.Unicode, nullable=False)
    password_hash = db.Column(db.LargeBinary) # hash is a binary attribute

    # make a write-only password property that just updates the stored hash
    @property
    def password(self):
        raise AttributeError("password is a write-only attribute")
    @password.setter
    def password(self, pwd: str) -> None:
        self.password_hash = password_hasher.hash(pwd)
    
    # add a verify_password convenience method
    def verify_password(self, pwd: str) -> bool:
        return password_hasher.check(pwd, self.password_hash)
    
class Status(db.Model):
    __tablename__ = 'Status'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Unicode, nullable=False)
    text = db.Column(db.Unicode, nullable=False)
    color = db.Column(db.Unicode, nullable=False) # To implement with ML...
    user = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    UserIsCurrentStatus = db.relationship('User', foreign_keys='User.currentStatusID', backref='currentStatus')

