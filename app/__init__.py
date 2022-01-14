import os
from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

app.config.from_object('config')

from . import auth
app.register_blueprint(auth.auth)

from . import posts
app.register_blueprint(posts.posts)

from . import user
app.register_blueprint(user.user)




