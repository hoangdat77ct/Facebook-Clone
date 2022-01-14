from flask import jsonify, Blueprint,request
from app.db import query_CUD, query_select
from app.auth import token_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

user = Blueprint("user",__name__)
CORS(user)

@user.route('api/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    sql = '''
    SELECT user_id,public_name, avatar, cover_img, phone, email FROM user
    '''
    users = query_select(sql)
    if not users:
        return jsonify({'message' : 'No user found!'})
    res = []
    for user in users:
        res.append({
            'user_id' : user[0],
            'user_name': user[1],
            'avatar' : user[2],
            'cover_img': user[3],
            'phone': user[4],
            'email' : user[5]
        })
    return jsonify({"user": res})


@user.route('api/user/<int:id>')
@token_required
def get_one_user(current_user,id):
    if request.method == "GET":
        if id:
            sql = '''
            SELECT user_id,public_name, avatar, cover_img, phone, email
            FROM user where user_id=%s
            '''
            value = (id, )
            user = query_select(sql,value)
            if not user:
                return jsonify({'message' : 'No user found!'})
            res = []
            res.append({
                'user_id' : user[0][0],
                'public_name': user[0][1],
                'avatar' : user[0][2],
                'cover_img': user[0][3],
                'phone': user[0][4],
                'email' : user[0][5]
                })
        return jsonify({"user": res})


@user.route("api/update-avatar", methods = ["PUT"])
@token_required
def update_avatar(current_user):
    if request.method == "PUT":
        try:
            data = request.get_json()
            avatar = data["avatar"]
            sql = '''
            UPDATE user SET avatar=%s where user_id=%s
            '''
            value = (avatar,current_user[0][0], )
            query_CUD(sql, value)
            return jsonify({"Message":"Successfully!"}),200
        except:
            return jsonify({'Message' : 'Failed!'}),400


@user.route("api/update-coverimg", methods = ["PUT"])
@token_required
def update_cover_img(current_user):
    if request.method == "PUT":
        try:
            data = request.get_json()

            cover_img = data["cover_img"]

            sql = '''
            UPDATE user SET cover_img=%s where user_id=%s
            '''
            values = (cover_img,current_user[0][0], )
            query_CUD(sql, values)
            return jsonify({"Message": "Successfully!"}),200
        except:
            return jsonify({'Message' : 'Failed!'}),400




@user.route("api/update-user", methods = ["PUT"])
@token_required
def update_user(current_user):
    if request.method == "PUT":
        try:
            data = request.get_json()
            public_name = data["public_name"]
            avatar = data["avatar"]
            cover_img = data["cover_img"]

            sql = '''
            UPDATE user SET public_name=%s, avatar=%s, cover_img=%s WHERE user_id=%s
            '''
            values = (public_name,avatar,cover_img,current_user[0][0], )
            query_CUD(sql, values)
            return jsonify({"Message": "Successfully!"}),200
        except:
            return jsonify({'Message' : 'Failed!'}),400


@user.route("api/update-password", methods = ["PUT"])
@token_required
def update_password(current_user):
    try:
        if request.method == "PUT":
            data = request.get_json()
            old_password = data["old_password"]
            new_password = data["new_password"]
            confirm_password = data["confirm_password"]

            if new_password != confirm_password:
                return jsonify({'Message' : 'Confirm password is not the same'})
            if old_password != new_password and check_password_hash(current_user[0][7],old_password):
                new_password = generate_password_hash(new_password,method='sha256')
                sql = '''
                UPDATE user SET password=%s WHERE user_id=%s
                '''
                value = (new_password,current_user[0][0], )
                query_CUD(sql, value)
                return jsonify({"Message": "Successfully!"}),200
    except:
        return jsonify({'Message' : 'Failed!'}),400
