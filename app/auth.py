from os import error
from flask import jsonify, Blueprint,request, make_response
from app.db import query_CUD, query_select
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import config

auth = Blueprint("auth",__name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, config.SECRET_KEY)
            sql = '''
            SELECT * FROM user where user_name = %s
            '''
            value = (data['username'], )
            current_user = query_select(sql, value)

        except error as e:
            return jsonify({'message' : e}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@auth.route("/api/login", methods = ["GET"])
def login():
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
        token = jwt.encode({'username' : user[0][0], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=30)}, config.SECRET_KEY)
        res = []
        res.append({
            "user_id": user[0][0],
            "public_name": user[0][1],
            "phone": user[0][4],
            "email": user[0][5],
            'token' : token.decode('UTF-8')
        })
        return jsonify({"user" : res}),200
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})


@auth.route("/api/register", methods=["POST"])
def register():
    if request.method == "POST":
        data = request.get_json()

        public_name = data["public_name"]
        user_name = data["user_name"]
        password = generate_password_hash(data['password'], method='sha256')
        phone = data["phone"]
        email = data["email"]

        sql = '''
        INSERT INTO user(public_name,user_name,password,phone,email) VALUES(%s,%s,%s,%s,%s)
        '''
        values = (public_name,user_name, password, phone, email, )
        query_CUD(sql, values)
        return jsonify({"Message":"Sign Up Success"}), 200
