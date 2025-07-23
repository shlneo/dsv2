from . import db
from flask_login import UserMixin

server_members = db.Table('server_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('server_id', db.Integer, db.ForeignKey('server.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  
    email = db.Column(db.String(50), unique=True)
    telephone = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(12), unique=True)
    birthday = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(), nullable=False)
    
    owned_servers = db.relationship('Server', backref='owner', lazy=True, cascade="all, delete-orphan")
    
    joined_servers = db.relationship('Server',
        secondary=server_members,
        backref=db.backref('members', lazy=True))

class Server(db.Model):
    __tablename__ = 'server'
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(50),  nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    channels = db.relationship('Channel', backref='server', lazy=True, cascade="all, delete-orphan")

channel_members = db.Table('channel_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('channel_id', db.Integer, db.ForeignKey('channel.id'), primary_key=True)
)

class Channel(db.Model):
    __tablename__ = 'channel'
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(50), nullable=False)
    is_text = db.Column(db.Boolean, default=False)
    is_voice = db.Column(db.Boolean, default=False)
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'), nullable=False)
    members = db.relationship('User', secondary=channel_members, backref=db.backref('channels', lazy='dynamic'))

class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp()) 
    
class Chat_message(db.Model):
    __tablename__ = 'chat_message'
    
    id = db.Column(db.Integer, primary_key=True)  
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  
    content = db.Column(db.Text, nullable=False) 
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp()) 
    chat = db.relationship('Chat', backref='messages')
    user = db.relationship('User', backref='messages')