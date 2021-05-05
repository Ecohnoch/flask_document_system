from app import app
from flask import render_template

@app.errorhandler(401)
def go_401(e):
    # app.logger.error("[401 Error] ", str(e))
    return render_template('errors/401.html')

@app.errorhandler(403)
def go_403(e):
    # app.logger.error("[403 error] ", str(e))
    return render_template('errors/403.html')

@app.errorhandler(404)
def go_404(e):
    # app.logger.error("[404 Error] ", str(e))
    return render_template('errors/404.html')