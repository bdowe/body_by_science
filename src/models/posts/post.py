from bson.objectid import ObjectId
from flask import session
from src.database import Database
from src.utils import Utils
import datetime

from src.models.users.user import User


class Post(object):
    @staticmethod
    def new(title, description, body, tag):
        email = session['email']
        if title and description and email and body:
            body = body.split(',')
            user = User.getByEmail(email)
            Database.insert('posts', {'title': title, 'description': description, 'body': body, "tag": tag, 'timestamp': datetime.datetime.now(), 'user_id': user['_id']})
            return True
        return False

    @staticmethod
    def update(post_id, title, description, body, tag):
        email = session['email']
        if title and description and email and body:
            body = body.split(',')
            user = User.getByEmail(email)
            Database.update('posts', {'_id': ObjectId(post_id)}, {'_id': ObjectId(post_id), 'title': title, 'description': description, 'body': body, "tag": tag,
                                      'timestamp': datetime.datetime.now(), 'user_id': user['_id']})
            return True
        return False

    @staticmethod
    def getOneById(post_id):
        if post_id:
            return Database.find_one('posts', {'_id': ObjectId(post_id)})
        return False

    @staticmethod
    def getOneByUserId(post_id, user_id):
        if post_id:
            return Database.find_one('posts', {'_id': ObjectId(post_id), 'user_id': user_id})
        return False

    @staticmethod
    def getAllByUserId(user_id):
        return Database.find('posts', {'user_id': user_id})

    @staticmethod
    def getAll():
        return Database.find('posts', {})

    @staticmethod
    def getManyByTag(tag):
        if tag is not None:
            return Database.find('posts', {'tag': tag})
        return None

    @staticmethod
    def delete(post_id):
        if post_id:
            Database.remove('posts', {'_id': ObjectId(post_id)})
            return True
        return False

    @staticmethod
    def getAllTags():
        return Database.find('tags', {})

    @staticmethod
    def tagExists(tag):
        return Database.find('tags', {"tag": tag}) is not None

    @classmethod
    def addTag(cls, tag):
        if tag:
            Database.insert('tags', {'tag': tag})
            return True
        return False
