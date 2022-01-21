from flask import jsonify, Blueprint,request
from app.db import query_CUD, query_select
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
import jwt
import config
from app import mail
from flask_mail import Message
import datetime

user = Blueprint("user",__name__)

@user.route('/api/user', methods=['GET'])
@jwt_required()
def get_all_users():
    sql = '''
    SELECT user_id,public_name, avatar, cover_img, phone, email,
    public_status, user_name FROM user
    '''
    users = query_select(sql)
    if not users:
        return jsonify({'message' : 'No user found!'})
    res = []
    for user in users:
        res.append({
            'user_id' : user[0],
            'user_name': user[7],
            'public_name': user[1],
            'public_status': user[6],
            'avatar' : user[2],
            'cover_img': user[3],
            'phone': user[4],
            'email' : user[5]
        })
    return jsonify({"user": res})


@user.route('/api/user/guest/', methods=['GET'])
def get_all_users_for_guest():
    sql = '''
    SELECT user_id, public_name, public_sttus, avatar, user_name FROM user
    '''
    users = query_select(sql)
    if not users:
        return jsonify({'message' : 'No user found!'})
    res = []
    for user in users:
        res.append({
            'user_id' : user[0],
            'user_name': user[4],
            'public_name': user[1],
            'public_status': user[2],
            'avatar' : user[3]
        })
    return jsonify({"user": res})


@user.route('/api/user/<string:user_name>')
def get_one_user_for_guest(user_name):
        sql = '''
            SELECT user_id,public_name, avatar, cover_img, phone, email,
            public_status, user_name FROM user where user_name=%s
            '''
        value = (user_name, )
        user = query_select(sql,value)
        if not user:
            return jsonify({'message' : 'No user found!'}),404
        res = {
            'user_id' : user[0][0],
            'public_name': user[0][1],
            'avatar' : user[0][2],
            'cover_img': user[0][3],
            'phone': user[0][4],
            'email' : user[0][5],
            'user_name': user[0][7],
            'public_status': user[0][6]
        }
        if user[0][6] == 0:
            return jsonify({'message' : 'User is in a non-public state'}),404
        return jsonify({"user": res})


@user.route('/api/user/<string:user_name>')
@jwt_required()
def get_one_user(user_name):
        sql = '''
            SELECT user_id,public_name, avatar, cover_img, phone, email,
            public_status, user_name FROM user where user_name=%s
            '''
        value = (user_name, )
        user = query_select(sql,value)
        if not user:
            return jsonify({'message' : 'No user found!'}),404
        res = {
            'user_id' : user[0][0],
            'public_name': user[0][1],
            'avatar' : user[0][2],
            'cover_img': user[0][3],
            'phone': user[0][4],
            'email' : user[0][5],
            'user_name': user[0][7],
            'public_status': user[0][6]
        }
        if user[0][0] != get_jwt_identity() and user[0][6] == 0:
            return jsonify({'message' : 'User is in a non-public state'}),404
        return jsonify({"user": res})


@user.route("/api/update-avatar", methods = ["PUT"])
@jwt_required()
def update_avatar():
    if request.method == "PUT":
        try:
            try:
                data = request.get_json()
                avatar = data["avatar"]
            except:
                return jsonify({"Message": "Field requied"}),422
            sql = '''
            UPDATE user SET avatar=%s where user_id=%s
            '''
            value = (avatar,get_jwt_identity(), )
            query_CUD(sql, value)
            return jsonify({"Message":"Successfully!"}),200
        except:
            return jsonify({'Message' : 'Failed!'}),400


@user.route("/api/update-coverimg", methods = ["PUT"])
@jwt_required()
def update_cover_img():
    if request.method == "PUT":
        try:
            try:
                data = request.get_json()
                cover_img = data["cover_img"]
            except:
                return jsonify({"Message": "Field requied"}),422
            sql = '''
            UPDATE user SET cover_img=%s where user_id=%s
            '''
            values = (cover_img,get_jwt_identity(), )
            query_CUD(sql, values)
            return jsonify({"Message": "Successfully!"}),200
        except:
            return jsonify({'Message' : 'Failed!'}),400


@user.route("/api/update-user", methods = ["PUT"])
@jwt_required()
def update_user():
    if request.method == "PUT":
        try:
            try:
                data = request.get_json()
                public_name = data["public_name"]
                avatar = data["avatar"]
                cover_img = data["cover_img"]
                public_status = data["public_status"]
            except:
                return jsonify({"Message": "Field requied"}),422
            sql = '''
            UPDATE user SET public_name=%s, avatar=%s, cover_img=%s, public_status=%s WHERE user_id=%s
            '''
            value = (public_name,avatar,cover_img,public_status,get_jwt_identity(), )
            query_CUD(sql, value)
            return jsonify({"Message": "Successfully!"}),200
        except:
            return jsonify({'Message' : 'Failed!'}),400


@user.route("/api/sreach", methods = ["GET"])
@jwt_required()
def sreach():
        try:
            key = request.args.get('keyword', None)
        except:
            return jsonify({"Message": "Field requied"}),422
        sql = f'''
        SELECT * FROM user WHERE public_name LIKE "%{key}%"
        and user_id!={get_jwt_identity()} and public_status=1
        '''
        print(sql)
        users = query_select(sql)
        if not users:
            return jsonify("")
        res = []
        for user in users:
            res.append({
                'user_id' : user[0],
                'user_name' : user[6],
                'public_name' : user[1],
                'phone': user[4],
                'avatar' : user[2],
            })
        return jsonify({"users": res}), 200


@user.route("/api/forgot-password", methods = ["GET","POST"])
def forgot_password():
    if request.method == "POST":
        try:
            data = request.get_json()
            email = data["email"]
        except:
            return jsonify({"Message": "Field requied"}),422
        token = jwt.encode({"email":email, 'exp' : datetime.datetime.utcnow() +
                datetime.timedelta(minutes=10)}, config.SECRET_KEY)
        content = f"""\
                Hi
                Visit the link to recover the password (link is valid for 10 minutes)
                Here is the link: http://127.0.0.1:5000/api/refresh-password/{token}
        """
        msg = Message("Forgot-password",body=content,
            sender="datnguyen.mkd@gmail.com",
            recipients=[data["email"]])
        mail.send(msg)
        return jsonify({"forgot-password" : token},"Sent a message!"),200



@user.route("/api/refresh-password/<string:token>", methods = ["GET","POST"])
def refresh_password(token=None):
    access_token=None
    if 'access-token-password' in request.headers:
        access_token = request.headers['access-token-password']
    if not access_token:
        return jsonify({'message' : 'Token is missing!'}), 401
    if token == access_token:
        try:
            if request.method == "POST":
                try:
                    data = request.get_json()
                    old_password = data["old_password"]
                    new_password = data["new_password"]
                    confirm_password = data["confirm_password"]
                except:
                    return jsonify({"Message": "Field requied"}),422
                data = jwt.decode(token, config.SECRET_KEY,algorithms="HS256")
                print(data)
                sql = '''
                SELECT * FROM user where email = %s
                '''
                value = (data['email'], )
                user_forgot_password = query_select(sql, value)
                print(user_forgot_password)
                if new_password != confirm_password:
                    return jsonify({'Message' : 'Confirm password is not the same'})

                if old_password != new_password and check_password_hash(user_forgot_password[0][7],old_password):
                    new_password = generate_password_hash(new_password,method='sha256')
                    sql = '''
                    UPDATE user SET password=%s WHERE user_id=%s
                    '''
                    value = (new_password,user_forgot_password[0][0], )
                    query_CUD(sql, value)
                    return jsonify({"Message": "Successfully!"}),200
        except:
            return jsonify({'Message' : 'Failed!'}),400
    else:
        return jsonify({'message' : 'Token is invalid!'}), 401
