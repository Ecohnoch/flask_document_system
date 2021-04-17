# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : __init__.py.py
# @Function : TODO

import os
import time
import traceback
from flask import render_template, Blueprint, request, jsonify, send_file

from docs.db import db_docs

import configs

docs_print = Blueprint('docs', __name__, template_folder='./templates')

@docs_print.route('/docs')
def docs_show():
    all_records = db_docs.find_all()
    input_records = []
    for each_record in all_records:
        each_record['href'] = '/docs/pages/' + str(each_record['id'])
        input_records.append(each_record)
    return render_template("default_documents.html", all_records=input_records)

@docs_print.route('/docs/document_upload')
def document_upload():
    return render_template("document_upload.html")

@docs_print.route('/docs/rename_page')
def document_rename_page():
    return render_template("document_rename_layer.html")

@docs_print.route('/docs/pages/<id>')
def docs_page_show(id):
    all_records = db_docs.find_all()
    input_records = []
    for each_record in all_records:
        each_record['href'] = '/docs/pages/' + str(each_record['id'])
        each_record['id'] = str(each_record['id'])
        each_record['now_id'] = id
        input_records.append(each_record)
    return render_template("template_documents.html", all_records=input_records)


@docs_print.route('/docs/submit_page')
def document_submit_page():
    return render_template("document_submit_layer.html")

@docs_print.route('/docs/delete', methods=['POST'])
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

@docs_print.route('/docs/rename/', methods=['POST'])
def document_rename():
    try:
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

@docs_print.route('/docs/get_docfile/uploaded_docs/<date_time>/<filename>')
def get_docfile(date_time, filename):
    tmp_dir = configs.app_store_dir
    return send_file(os.path.join(tmp_dir, 'uploaded_docs', date_time, filename))

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['pdf', 'html'])
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@docs_print.route('/docs/upload/', methods=['POST'])
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