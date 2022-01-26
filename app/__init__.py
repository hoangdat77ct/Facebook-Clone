import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail

app = Flask(__name__)
jwt = JWTManager()
mail = Mail(app)

CORS(app, resources=r'/api/*')
app.config.from_object('config')
jwt.init_app(app)
mail.init_app(app)

from . import auth
app.register_blueprint(auth.auth)

from . import posts
app.register_blueprint(posts.posts)

from . import user
app.register_blueprint(user.user)

from . import admin
app.register_blueprint(admin.admin)