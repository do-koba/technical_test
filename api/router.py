from flask import Flask, redirect
from flasgger import Swagger

from api.routes import data_bp

app = Flask(__name__)
swagger = Swagger(app)


@app.route('/')
def redirect_to_swagger():
    return redirect('/apidocs/')


app.register_blueprint(data_bp, url_prefix='/data')
