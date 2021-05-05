# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : db_docs.py.py
# @Function : TODO


from app import app, mongo
from bson.objectid import ObjectId


def insert_one(data, allow_repeat=True):
    find_ans = find_one({'id': data['id']})
    if find_ans and allow_repeat:
        mongo.db.docs_comments.save(data)
        return
    if find_ans and not allow_repeat:
        raise RuntimeError('*** 已经存在：', find_ans)

    mongo.db.docs_comments.insert_one(data)

def delete_one(data, allow_empty=True):
    find_ans = find_one({'id': data['id']})
    if find_ans:
        mongo.db.docs_comments.delete_one(data)
        return
    if not find_ans and allow_empty:
        return
    raise RuntimeError("*** 删除数据为空: ", data)


def update_one(data, log=True):
    find_ans = find_one({'id': data['id']})
    if find_ans:
        mongo.db.docs_comments.save(data)
        return
    raise RuntimeError("*** 更新数据为空: ", data)


def find_one(key_value):
    ans = mongo.db.docs_comments.find_one(key_value)
    if not ans:
        return ans
    return ans


def find_all(with_id=True):
    cursor = mongo.db.docs_comments.find()
    ans = []
    for each_data in cursor:
        if not with_id:
            each_data.pop('_id')
        ans.append(each_data)
    return ans


def find_all_with_doc_id(doc_id, with_id=True):
    cursor = mongo.db.docs_comments.find({'doc_id': doc_id})
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
    return mongo.db.docs_comments.find().count()


def get_tasks_count_with_doc_id(doc_id):
    return mongo.db.docs_comments.find({'doc_id': doc_id}).count()

def get_last_tasks_id():
    all_tasks = mongo.db.docs_comments.find()
    max_id = 0
    for each_task in all_tasks:
        if max_id < each_task['id']:
            max_id = each_task['id']
    return max_id

