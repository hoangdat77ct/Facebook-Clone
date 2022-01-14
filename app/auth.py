from os import error
from flask import jsonify, Blueprint,request, make_response
from app.db import query_CUD, query_select
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import config
from flask_cors import CORS

auth = Blueprint("auth",__name__)
CORS(auth)


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

@auth.route("api/login", methods = ["GET"])
def login():
    auth = request.authorization
    if not auth or not auth.password or not auth.username:
        return make_response("Could not verify",401, {"WWW-Authenticate"})
    sql = '''
    SELECT user_name, password FROM user where user_name = %s
    '''
    value = (auth.username, )
    user = query_select(sql, value)
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if auth.username == user[0][0] and check_password_hash(user[0][1],auth.password):
        token = jwt.encode({'username' : user[0][0], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=30)}, config.SECRET_KEY)
        return jsonify({'token' : token.decode('UTF-8')})
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})


@auth.route("api/register", methods=["POST"])
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
