# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : run.py
# @Function : TODO

from app  import app
from docs import docs_print

import configs

app.register_blueprint(docs_print)

if __name__ == '__main__':
    app.run(port=configs.web_port)