from flask import jsonify, Blueprint,request
from app.db import query_CUD, query_select
import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash


admin = Blueprint("admin",__name__)


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
            return jsonify({"Message": "Successfully!"}),200
        except:
            return jsonify({'Message' : 'Failed!'}),400



@admin.route('/api/admin/delete-user/<int:user_id>', methods=['PUT'])
@jwt_required()
def delete_user(user_id=None):
    if request.method == "PUT":
        try:
            sql = '''
            DELETE FROM user WHERE user_id=%s
            '''
            value = (user_id, )
            res=query_CUD(sql, value)
            return jsonify({"Message": "Successfully!"}),200
        except:
            return jsonify({'Message' : 'Failed!'}),400





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
            return jsonify({"Message": "Successfully"}),200


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
            return jsonify({"Post deleted": True}), 200


