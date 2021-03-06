import re
import requests
from passlib.hash import pbkdf2_sha512
import src.constants as Constants

class Utils(object):
    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile('^[\w-]+@([\w-]+\.)+[\w-]+$')
        return True if email_address_matcher.match(email) else False

    @staticmethod
    def hash_password(password):
        """
        Hashes a password using pbkdf2_sha512
        :param password: The sha512 password from the Login/register form
        :return: a sha512->pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks that the password the user sent matches
        that of the database.
        The database password is encrypted more than the user's
        password at this stage
        :param password: sha512-hashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if passwords match and false otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)

    @classmethod
    def send_contact_message(cls, name, email, body):
        valid = cls.email_is_valid(email)
        if name and email and valid and body:
            return requests.post(
                Constants.URL,
                auth=("api", Constants.API_KEY),
                data={
                    "from": Constants.FROM,
                    "to": Constants.EMAIL,
                    "subject": "New message from Body By Science!",
                    "text": "Name: " + name + ", Email: " + email + ", message:" + body
                }
            )
        return False
