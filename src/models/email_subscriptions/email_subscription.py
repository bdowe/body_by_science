from src.database import Database
from src.utils import Utils
import datetime


class EmailSubscription(object):
    @classmethod
    def new(cls, email):
        if email:
            subscription = cls.getByEmail(email)
            valid = Utils.email_is_valid(email)
            if not subscription and valid:
                Database.insert('email_subscriptions', {'email': email, 'timestamp': datetime.datetime.now()})
                return True
        return False

    @staticmethod
    def getByEmail(email):
        if email:
            subscription = Database.find_one('email_subscriptions', {'email': email})
            if subscription:
                return subscription
        return None

    @staticmethod
    def getAll():
        return Database.find('email_subscriptions', {})

    @staticmethod
    def delete(email):
        if email:
            Database.remove('email_subscriptions', {'email': email})
            return True
        return False