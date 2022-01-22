import random
from flask import jsonify, Blueprint,request,send_file
from app.db import query_CUD, query_select
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from werkzeug.utils import secure_filename
import config

posts = Blueprint("posts",__name__)

@posts.route('/api/post/<int:id>')
@jwt_required()
def get_one_post(id=None):
    sql = '''
        SELECT `article_id`, article.`user_id`, `content`, `static_file`,
        `publish_time`, `status`, user.public_name FROM `article`,`user`
        WHERE article.user_id=user.user_id and article_id=%s
        '''
    value = (id, )
    posts = query_select(sql,value)
    if not posts:
        return jsonify({'message' : 'No post found!'})
    res = {
        'user_id' : posts[0][1],
        'user_name': posts[0][6],
        'article_id': posts[0][0],
        'content' : posts[0][2],
        'static_file': posts[0][3],
        'publish_time': str(posts[0][4]),
        'status' : posts[0][5]
    }
    return jsonify({"posts": res})


@posts.route("/api/posts")
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
        return jsonify({'message' : 'Failed'}),404


@posts.route('/api/posts/<int:user_id>')
@jwt_required()
def get_all_posts_by_user_id(user_id=None):
        sql = '''
            SELECT `article_id`, article.`user_id`, `content`, `static_file`,
            `publish_time`, `status`, user.public_name FROM `article`,`user`
            WHERE article.user_id=user.user_id and article.user_id=%s
            '''
        value = (user_id, )
        posts = query_select(sql, value)
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


@posts.route('/api/posts-for-guest/<int:user_id>')
def get_all_posts_by_user_id_for_guest(user_id=None):
        sql = '''
            SELECT `article_id`, article.`user_id`, `content`, `static_file`,
            `publish_time`, `status`, user.public_name FROM `article`,`user`
            WHERE article.user_id=user.user_id and article.user_id=%s
            '''
        value = (user_id, )
        posts = query_select(sql, value)
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


"""
@posts.route('/api/all-posts/<int:user_id>')
@jwt_required()
def get_all_posts_status(user_id):
    if get_jwt_identity() != user_id:
        sql = '''
            SELECT `article_id`, article.`user_id`, `content`, `static_file`,
            `publish_time`, `status`, user.public_name FROM `article`,`user`
            WHERE article.user_id=user.user_id and article.user_id=%s and status=1
            '''
        value = (user_id, )
        posts = query_select(sql, value)
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
    else:
        sql = '''
            SELECT `article_id`, article.`user_id`, `content`, `static_file`,
            `publish_time`, `status`, user.public_name FROM `article`,`user`
            WHERE article.user_id=user.user_id and article.user_id=%s
            '''
        value = (user_id, )
        posts = query_select(sql, value)
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
"""


@posts.route("/api/add-post",methods=["POST"])
@jwt_required()
def add_post():
    if request.method == "POST":
        try:
            data = request.get_json()
            user_id = get_jwt_identity()
            content = data["content"]
            static_file = data['static_file']
            status = data["status"]

        except:
            return jsonify({"Message": "Field requied"}),422
        if not content: #and not static_file:
            return jsonify({"Fail"}),404
        sql = '''
        INSERT INTO article(user_id,content,static_file,publish_time,status)
        VALUES(%s,%s,%s,NOW(),%s)
        '''
        values = (user_id,content,static_file,status, )
        res=query_CUD(sql, values)
        return jsonify({"Message": "Post successfully!!!"}),200


@posts.route("/api/update-post/<int:id>", methods = ["PUT"])
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
            UPDATE article SET content=%s, static_file=%s, status=%s where article_id = %s and user_id=%s
            '''
            value = (content,static_file,status,id,get_jwt_identity(), )
            query_CUD(sql, value)
            return jsonify({"Message": "Successfully"}),200


@posts.route("/api/delete-post/<int:id>", methods = ["DELETE"])
@jwt_required()
def delete_post(id=None):
    if request.method == "DELETE":
        if id:
            sql = '''
            DELETE FROM article where article_id=%s and user_id=%s
            '''
            value = (id,get_jwt_identity(), )
            query_CUD(sql, value)
            return jsonify({"Post deleted": True}), 200



ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@posts.route('/api/multiple-files-upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return jsonify({'message' : 'No file part in the request'}), 400
    files = request.files.getlist('files')
    errors = {}
    success = False
    for file in files:
        if file and allowed_file(file.filename):
            val = random.randint(100000,9999999)
            format_img = os.path.splitext(file.filename)
            filename = secure_filename(str(val)+format_img[1])
            file.save(os.path.join(config.UPLOAD_FOLDER, filename))
            success = True
        else:
            errors[file.filename] = 'File type is not allowed'
    if success and errors:
        errors[file.filename] = 'File type is not allowed'
        return jsonify(errors), 500
    if success:
        return jsonify({'filename': filename,'message' : 'Files successfully uploaded'}), 201
    else:
        return jsonify(errors), 500


@posts.route('/api/get-img/<string:file>')
def get_img(file=None):
    if file == None:
        return jsonify({'message' : 'No file found!'})
    filename = config.UPLOAD_FOLDER+file
    return send_file(filename)
