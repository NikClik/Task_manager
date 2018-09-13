from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pack.db.tables import User
from pack.setting import *

engine = create_engine(str(connect_str_to_db()))
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class UsersFunctions:

    @classmethod
    def get_all_users(cls):
        users = session.query(User).all()
        session.close()
        return users

    @classmethod
    def add_user(cls, user):
        session.add(user)
        session.commit()
        session.close()

    @classmethod
    def change_user_password(cls, user, new_password):
        session.query(User).filter(User.login == user.login and User.password == user.password and
                                   User.question == user.question and User.answer == user.answer)\
            .update({"password": (new_password, )})
        session.commit()
        session.close()

    @classmethod
    def get_user_by_login(cls, login):
        users = session.query(User).filter(User.login == login).first()
        session.close()
        return users

    @classmethod
    def get_user_by_login_and_password(cls, login, password):
        users = session.query(User).filter(User.login == login and User.password == password).first()
        session.close()
        return users
