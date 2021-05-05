# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : run.py
# @Function : TODO

from app  import app
from errors import *
from login.app.web_login import login_print
from docs import docs_print
import configs

app.register_blueprint(login_print)
app.register_blueprint(docs_print)

if __name__ == '__main__':
    app.run(port=configs.web_port)