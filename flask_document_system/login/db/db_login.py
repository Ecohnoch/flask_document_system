from app import app, mongo
from login.app.permission import Permission

def get_user_info_from_user_id(user_id):
    user = mongo.db.users.find_one({'username': user_id})
    app.logger.debug("[LOGIN][GET USER]: {}".format(user_id))
    return user

def verify_login(username, password):
    user = mongo.db.users.find_one({'username': username, 'password': password})
    if not user:
        app.logger.debug("[LOGIN][VERIFY] Failed, username: {}".format(username))
        return False
    app.logger.debug("[LOGIN][VERIFY] OK, username: {}".format(username))
    return True

def add_new_user(new_user):
    if mongo.db.users.find_one({'username': new_user['username']}):
        return -1
    return mongo.db.users.insert_one(new_user)


def get_user_permission_from_user_id(user_id):
    user = mongo.db.users.find_one({'username': user_id})
    permission = Permission.load_permission(user['permission'])
    app.logger.debug("[LOGIN][GET_PERMISSION] Failed, username: {}, permission: {}".format(user_id, permission))
    return permission