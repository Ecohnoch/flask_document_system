# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : __init__.py.py
# @Function : TODO

import os
import time
import traceback
import flask_login
from flask import render_template, Blueprint, request, jsonify, send_file

from docs.db import db_docs, db_docs_comments
from login import member_required

import configs

docs_print = Blueprint('docs', __name__, template_folder='./templates')

@docs_print.route('/web/now_user', methods=['GET', 'POST'])
@flask_login.login_required
def get_now_user():
    try:
        now_user = str(flask_login.current_user.id)
        return {'status': 200, 'now_user': now_user}
    except Exception as e:
        return {'status': 500, 'now_user': 'ERROR'}

@docs_print.route('/')
@flask_login.login_required
def docs_show():
    all_records = db_docs.find_all()
    input_records = []
    for each_record in all_records:
        each_record['href'] = '/docs/pages/' + str(each_record['id'])
        input_records.append(each_record)
    return render_template("default_documents.html", all_records=input_records)

@docs_print.route('/docs/pages/<id>')
@flask_login.login_required
def docs_page_show(id):
    all_records = db_docs.find_all()
    input_records = []
    for each_record in all_records:
        each_record['href'] = '/docs/pages/' + str(each_record['id'])
        each_record['id'] = str(each_record['id'])
        each_record['now_id'] = id
        input_records.append(each_record)

    query_comments = db_docs_comments.find_all_with_doc_id(doc_id=float(id))
    comments = []
    for each_comment in query_comments:
        each_comment['title'] = each_comment['owner'] + ' | ' + each_comment['create_date']
        comments.append(each_comment)

    return render_template("template_documents.html", all_records=input_records, comments=comments)

@docs_print.route('/docs/document_upload')
@flask_login.login_required
def document_upload():
    return render_template("document_upload.html")

@docs_print.route('/docs/rename_page')
@flask_login.login_required
def document_rename_page():
    return render_template("document_rename_layer.html")

@docs_print.route('/docs/comment_page')
@flask_login.login_required
def document_comment_page():
    return render_template("document_comment_layer.html")


@docs_print.route('/docs/submit_page')
@flask_login.login_required
def document_submit_page():
    return render_template("document_submit_layer.html")

@docs_print.route('/docs/delete', methods=['POST'])
@member_required
def document_delete():
    try:
        url = request.form.get('url')
        url = url.strip('\'')
        url = url.strip('/')
        now_id = float(url.split('/')[-1])
        db_docs.delete_one({'id': now_id})
        return {'result': 'OK'}

    except Exception as e:
        return {'result': str(e)}

@docs_print.route('/docs/delete_comment', methods=['POST'])
@flask_login.login_required
def document_delete_comment():
    try:
        comment_id = request.form.get('comment_id')
        comment_item = db_docs_comments.find_one({'id': float(comment_id)})

        if flask_login.current_user.id != comment_item['owner'] and not flask_login.current_user.is_admin():
            return {'result': str(403)}

        db_docs_comments.delete_one({'id': float(comment_id)})
        return {'result': 'OK'}

    except Exception as e:
        return {'result': str(e)}

@docs_print.route('/docs/rename/', methods=['POST'])
@flask_login.login_required
def document_rename():
    try:
        if not flask_login.current_user.upper_member():
            return {'result': '403'}
        url = request.form.get('url')
        name = request.form.get('name')
        url = url.strip('\'')
        url = url.strip('/')
        now_id = float(url.split('/')[-1])
        data = db_docs.find_one({'id': now_id})
        data['name'] = name
        db_docs.update_one(data)
        return {'result': 'OK'}

    except Exception as e:
        return {'result': str(e)}



@docs_print.route('/docs/submit/', methods=['POST'])
@flask_login.login_required
def document_submit():
    try:
        name  = request.form.get('name')
        doc_type = request.form.get('doc_type')
        now_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '-' + str(
            time.time() - int(time.time()))[2:5]
        doc_path = request.form.get('path')

        now_id = db_docs.get_last_tasks_id() + 1

        record = {
            'name': name,
            'doc_type': doc_type,
            'upload_time': now_time,
            'path': doc_path,
            'id': now_id
        }

        db_docs.insert_one(record)
        return {'message': "OK"}
    except Exception as e:
        traceback.print_exc()
        return {'message': "Fail", 'err_msg': str(e)}

@docs_print.route('/docs/comment/', methods=['POST'])
@flask_login.login_required
def document_comment():
    try:
        url = request.form.get('url')
        comment = request.form.get('comment')
        url = url.strip('\'')
        url = url.strip('/')
        doc_id = float(url.split('/')[-1])

        comment_item = {
            'id': db_docs_comments.get_last_tasks_id() + 1,
            'doc_id': doc_id,
            'comment': comment,
            'owner': flask_login.current_user.id,
            'create_date': time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        }
        db_docs_comments.insert_one(comment_item)
        return {'result': 'OK'}

    except Exception as e:
        return {'result': str(e)}

@docs_print.route('/docs/get_docfile/uploaded_docs/<date_time>/<filename>')
@flask_login.login_required
def get_docfile(date_time, filename):
    tmp_dir = configs.app_store_dir
    return send_file(os.path.join(tmp_dir, 'uploaded_docs', date_time, filename))

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['pdf', 'html'])
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@docs_print.route('/docs/upload/', methods=['POST'])
@flask_login.login_required
def document_upload_files():
    file = request.files['file']
    if file and allowed_file(file.filename):
        now_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '-' + str(
            time.time() - int(time.time()))[2:5]

        tmp_dir = configs.app_store_dir
        save_dir = os.path.join(tmp_dir, 'uploaded_docs')

        file_dir = os.path.join(save_dir, now_time)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        file_save_path = os.path.join(file_dir, file.filename)
        try:
            file.save(file_save_path)
            return jsonify({'status': 'success', 'path': os.path.join('uploaded_docs',
                         now_time, file.filename), 'err_msg': ''})
        except OSError:
            return jsonify({'status': 'error', 'path': '', 'err_msg': '未知错误'})