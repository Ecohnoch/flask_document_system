# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : configs.py
# @Function : TODO


app_secret_key    = 'your_secret_key'
app_database_host = 'mongo' # if don't use docker, so this is 'localhost'
app_database_name = 'docs'
app_database_user = 'your_user'
app_database_pwd  = 'your_pwd'
app_database_port = 27017

app_mongo_uri  = "mongodb://{}:{}@{}:{}/{}".format(
    app_database_user,
    app_database_pwd,
    app_database_host,
    app_database_port,
    app_database_name
)

app_store_dir  = './stored_doc_dir'

web_port = 10086