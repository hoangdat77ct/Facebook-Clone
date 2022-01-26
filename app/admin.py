from flask import jsonify, Blueprint,request
from app.db import query_CUD, query_select
import datetime
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash


admin = Blueprint("admin",__name__)


@admin.route('/api/admin/users', methods=['GET'])
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


@admin.route('/api/admin/add-user', methods=['GET',"POST"])
@jwt_required()
def add_user():
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
        values = (public_name,user_name,password,phone,email )
        res = query_CUD(sql, values)
        return jsonify({"Message":"Sign Up Success"}), 200


@admin.route('/api/admin/update-user/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id=None):
    if request.method == "PUT":
        try:
            data = request.get_json()
            public_name = data["public_name"]
            avatar = data["avatar"]
            cover_img = data["cover_img"]
            phone = data["phone"]
            email = data["email"]
            user_name = data["user_name"]
            password = generate_password_hash(data['password'], method='sha256')
        except:
            return jsonify({"Message": "Field requied"}),422
        sql = '''
        UPDATE user SET public_name=%s, avatar=%s, cover_img=%s, phone=%s, email=%s, user_name=%s,
        password=%s WHERE user_id=%s
        '''
        value = (public_name,avatar,cover_img,phone,email,user_name,password,user_id, )
        res=query_CUD(sql, value)
        if res == 1:
            return jsonify({"Message": "Successfully!"}),200
        else:
            return jsonify({'Message' : 'Failed!'}),400



@admin.route('/api/admin/delete-user/<int:user_id>', methods=['PUT'])
@jwt_required()
def delete_user(user_id=None):
    if request.method == "PUT":
        sql = '''
        DELETE FROM user WHERE user_id=%s
        '''
        value = (user_id, )
        res=query_CUD(sql, value)
        if res == 1:
            return jsonify({"Message": "Successfully!"}),200
        else:
            return jsonify({'Message' : 'Failed!'}),400


@admin.route("/api/posts")
@jwt_required()
def get_all_posts():
    try:
        sql = '''
            SELECT `article_id`, article.`user_id`, `content`, `static_file`,
            `publish_time`, `status`, user.public_name FROM `article`,`user`
            WHERE article.user_id=user.user_id
            '''
        posts = query_select(sql)
        if not posts:
            return jsonify({'message' : 'No posts found!'})
        res = []
        for post in posts:
            res.append({
                'user_id' : post[1],
                'user_name': post[6],
                'article_id': post[0],
                'content' : post[2],
                'static_file': post[3],
                'publish_time': post[4],
                'status' : post[5]
            })
        return jsonify({"posts": res})
    except:
        return jsonify({'message' : 'Failed'}),400

@admin.route("/api/admin/update-post/<int:id>", methods = ["PUT"])
@jwt_required()
def update_post(id=None):
    if request.method == "PUT":
        if id:
            try:
                data = request.get_json()
                content = data["content"]
                static_file = data["static_file"]
                status = data["status"]
            except:
                return jsonify({"Message": "Field requied"}),422
            sql = '''
            UPDATE article SET content=%s, static_file=%s, status=%s where article_id = %s
            '''
            value = (content,static_file,status,id, )
            res = query_CUD(sql, value)
            if res == 1:
                return jsonify({"Message": "Successfully"}),200
            else:
                return jsonify({'message' : 'Failed'}),400


@admin.route("/api/admin/delete-post/<int:id>", methods = ["DELETE"])
@jwt_required()
def delete_post(id=None):
    if request.method == "DELETE":
        if id:
            sql = '''
            DELETE FROM article where article_id=%s
            '''
            value = (id, )
            res = query_CUD(sql, value)
            if res == 1:
                return jsonify({"Post deleted": True}), 200
            else:
                return jsonify({'message' : 'Failed'}),400
