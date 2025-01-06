from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship,declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey,create_engine

engine = create_engine('sqlite:///C:/Users/Korisnik/PycharmProjects/pythonProject/Trading app/Trading-flask-webapp/instance/database.db')
Model = declarative_base()

class User(Model, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(150), unique=True)
    password =Column(String(1000))
    first_name = Column(String(150))
    coins = relationship('CryptoCoin', back_populates='user')
class CryptoCoin(Model):
    __tablename__ = 'crypto_coin'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True)
    price = Column(String(150))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User',back_populates='coins')
Model.metadata.create_all(engine)