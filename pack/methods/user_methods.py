from sqlalchemy.exc import *
from pack.functions.user_functions import UsersFunctions
from pack.db.tables import User


class UserMethods:

    @classmethod
    def registration(cls, login, password, question, answer):
        try:
            user = User(login=login, password=password, question=question, answer=answer)
            UsersFunctions.add_user(user)
        except IntegrityError as e:
            exception = e.args[0]
            print(exception[120:])

    @classmethod
    def change_password(cls, login, password, new_password, question, answer):
        user = UsersFunctions.get_user_by_login_and_password(login, password)
        if user is None:
            print("Данного пользователя не существует, проверьте пароль")
        else:
            user = User(login=login, password=password, question=question, answer=answer)
            UsersFunctions.change_user_password(user, new_password)


