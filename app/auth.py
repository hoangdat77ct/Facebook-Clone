from flask import jsonify, Blueprint,request, make_response
from app.db import query_CUD, query_select
from werkzeug.security import generate_password_hash, check_password_hash
from app import jwt
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required,
    get_jwt_identity
)


auth = Blueprint("auth",__name__)


@auth.route("/api/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@auth.route("/api/login", methods = ["POST"])
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
