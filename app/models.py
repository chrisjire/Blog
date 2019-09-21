from . import db 
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime 

@login_manager.use_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True) 
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    
    pitch = db.relationship('Pitch',backref = 'users',lazy="dynamic")
    
    comments = db.relationship('Comment',backref = 'user',lazy = "dynamic")
    
    def save_user(self):
        db.session.add(self)
        db.session.commit()
        
    def __repr__(self):
        return f'User {self.username}'