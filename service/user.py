import base64
import hashlib

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        user = self.dao.get_one(uid)
        if not user:
            return "", 404
        return user

    def get_all(self):
        return self.dao.get_all()

    def get_filter(self, filter_dict):
        filter_dict_clear = {}
        for key, value in filter_dict.items():
            if value is not None:
                filter_dict_clear[key] = value
        return self.dao.get_filter(filter_dict_clear)

    def create(self, user_d):
        user_pass = user_d.get('password')
        if user_pass:
            user_d['password'] = get_hash(user_pass)
        return self.dao.create(user_d)

    def update(self, user_d):
        user_pass = user_d.get('password')
        if user_pass:
            user_d['password'] = get_hash(user_pass)
        return self.dao.update(user_d)

    def delete(self, uid):
        user = self.get_one(uid)
        if user:
            self.session.delete(user)
            self.session.commit()
            return user
        return None
        # return self.dao.delete(uid)

# def get_hash(password):
#     return base64.b64encode(hashlib.pbkdf2_hmac(
#             'sha256',
#             password.encode('utf-8'),
#             PWD_HASH_SALT,
#             PWD_HASH_ITERATIONS
#         ))

def get_hash(password):
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),  # Convert the password to bytes
        PWD_HASH_SALT,
        PWD_HASH_ITERATIONS
    ).decode("utf-8", "ignore")

   #########
    #
    # def update(self, user_d):
    #     user = self.get_one(user_d.get("id"))
    #     if user:
    #         if user_d.get('username'):
    #             user.username = user_d.get('username')
    #         if user_d.get('password'):
    #             user.password = user_d.get('password')
    #         if user_d.get('role'):
    #             user.role = user_d.get('role')
    #
    #         self.session.add(user)
    #         self.session.commit()
    #         return user
    #     return None
