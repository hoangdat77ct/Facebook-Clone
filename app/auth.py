import datetime
from flask import jsonify, Blueprint,request, make_response
from app.db import query_CUD, query_select
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required,
    get_jwt_identity
)
import jwt
import config
from app import mail
from flask_mail import Message

auth = Blueprint("auth",__name__)


@auth.route("/api/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@auth.route("/api/login", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        auth = request.authorization
        if not auth or not auth.password or not auth.username:
            return make_response("Could not verify",401, {"WWW-Authenticate"})
        sql = '''
        SELECT * FROM user where user_name = %s
        '''
        value = (auth.username, )
        user = query_select(sql, value)
        if not user:
            return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
        if auth.username == user[0][6] and check_password_hash(user[0][7],auth.password):
            access_token = create_access_token(identity=user[0][0])
            refresh_token = create_refresh_token(identity=user[0][0])
            res = {
                "user_id": user[0][0],
                "public_name": user[0][1],
                "phone": user[0][4],
                "email": user[0][5],
                "token" : access_token,
                "refresh_token": refresh_token
            }
            return jsonify({"user": res}),200
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})


@auth.route("/api/register_user", methods=["GET","POST"])
def register():
    if request.method == "POST":
        data = request.get_json()
        res = {
            "public_name" : data["public_name"],
            "user_name" : data["user_name"],
            "password" : generate_password_hash(data['password'], method='sha256'),
            "phone" : data["phone"],
            "email" : data["email"]
        }
        token = jwt.encode({"register_user":res, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, config.SECRET_KEY)
        content = f"""\
            Dear {data["public_name"]},
            This is the link to verify your account registration on the web: XXX. You access the link to confirm the registration (link is valid for 10 minutes)
            Here is the link: http://127.0.0.1:5000/api/confirm/{token}
            Thanks,
            X
        """
        msg = Message("Registration verification",body=content,
                sender="datnguyen.mkd@gmail.com",
                recipients=[data["email"]])
        mail.send(msg)
        return jsonify({"register_token" : token},"Sent a message!"),200


@auth.route("/api/confirm/<string:token>", methods=["POST"])
def confirm(token=None):
    access_token=None
    if 'access-token-register' in request.headers:
        access_token = request.headers['access-token-register']

    if not access_token:
        return jsonify({'message' : 'Token is missing!'}), 401
    if token == access_token:
        try:
            data = jwt.decode(token, config.SECRET_KEY,algorithms="HS256")
            print(data)
            sql = '''
            INSERT INTO user(public_name,user_name,password,phone,email) VALUES(%s,%s,%s,%s,%s)
            '''
            values = (data['register_user']['public_name'],data['register_user']['user_name'], 
            data['register_user']['password'], data['register_user']['phone'], data['register_user']['email'], )
            query_CUD(sql, values)
            return jsonify({"Message":"Sign Up Success"}), 200
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401
    else:
        return jsonify({'message' : 'Token is invalid!'}), 401
