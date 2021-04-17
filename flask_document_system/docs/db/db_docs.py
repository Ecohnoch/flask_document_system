# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : db_docs.py.py
# @Function : TODO


from app import app, mongo
from bson.objectid import ObjectId

import configs

def insert_one(data, allow_repeat=True):
    find_ans = find_one({'id': data['id']})
    if find_ans and allow_repeat:
        eval('mongo.db.{}.docs.save(data)'.format(configs.app_database_name))
        return
    if find_ans and not allow_repeat:
        raise RuntimeError('*** Has existed', find_ans)
    eval('mongo.db.{}.docs.insert_one(data)'.format(configs.app_database_name))

def delete_one(data, allow_empty=True):
    find_ans = find_one({'id': data['id']})
    if find_ans:
        eval('mongo.db.{}.docs.delete_one(data)'.format(configs.app_database_name))
        return
    if not find_ans and allow_empty:
        return
    raise RuntimeError("*** Delete Error: ", data)


def update_one(data, log=True):
    find_ans = find_one({'id': data['id']})
    if find_ans:
        eval('mongo.db.{}.docs.save(data)'.format(configs.app_database_name))
        return
    raise RuntimeError("*** 更新数据为空: ", data)


def find_one(key_value):
    ans = eval('mongo.db.{}.docs.find_one(key_value)'.format(configs.app_database_name))
    if not ans:
        return ans
    return ans


def find_all(with_id=True):
    cursor = eval('mongo.db.{}.docs.find()'.format(configs.app_database_name))
    ans = []
    for each_data in cursor:
        if not with_id:
            each_data.pop('_id')
        ans.append(each_data)
    return ans

def save_all(data_list):
    for each_data in data_list:
        update_one(each_data, log=False)

def get_tasks_count():
    return eval('mongo.db.{}.docs.find().count()'.format(configs.app_database_name))

def get_last_tasks_id():
    all_tasks = eval('mongo.db.{}.docs.find()'.format(configs.app_database_name))
    max_id = 0
    for each_task in all_tasks:
        if max_id < each_task['id']:
            max_id = each_task['id']
    return max_id

