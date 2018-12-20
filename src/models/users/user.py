from flask import session
from src.database import Database
from src.utils import Utils


class User(object):
    @staticmethod
    def register(email, password):
        if email and password:
            user = User.getByEmail(email)
            if not user:
                password = Utils.hash_password(password)
                Database.insert('users', {'email': email, 'password': password})
                session['email'] = email
                return True
        return False

    @staticmethod
    def isLoginValid(email, password):
        if email and password:
            user = User.getByEmail(email)
            if user:
                return Utils.check_hashed_password(password, user['password'])
        return False

    @staticmethod
    def logout():
        session['email'] = None

    @staticmethod
    def getByEmail(email):
        if email:
            user = Database.find_one('users', {'email': email})
            if user:
                return user
        return None