from flask import session
from src.database import Database
from src.utils import Utils


class User(object):
    @classmethod
    def register(cls, email, password):
        if email and password:
            user = cls.getByEmail(email)
            if not user:
                password = Utils.hash_password(password)
                Database.insert('users', {'email': email, 'password': password})
                session['email'] = email
                return True
        return False

    @classmethod
    def isLoginValid(cls, email, password):
        if email and password:
            user = cls.getByEmail(email)
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