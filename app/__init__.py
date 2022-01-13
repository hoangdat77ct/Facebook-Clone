import os
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from . import auth
app.register_blueprint(auth.auth)

from . import posts
app.register_blueprint(posts.posts)

from . import user
app.register_blueprint(user.user)




