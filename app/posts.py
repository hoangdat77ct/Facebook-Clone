from flask import jsonify, Blueprint,request
from app.db import query_CUD, query_select
from flask_jwt_extended import jwt_required, get_jwt_identity


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
    res = []
    res.append({
        'user_id' : posts[0][1],
        'user_name': posts[0][6],
        'content' : posts[0][2],
        'static_file': posts[0][3],
        'publish_time': str(posts[0][4]),
        'status' : posts[0][5]
    })
    return jsonify({"posts": res})


@posts.route('/api/posts/<int:user_id>')
@jwt_required()
def get_all_posts(user_id):
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
                'content' : post[2],
                'static_file': post[3],
                'publish_time': post[4],
                'status' : post[5]
            })

    return jsonify({"posts": res})


@posts.route("/api/add-post",methods=["POST"])
@jwt_required()
def add_post():
    if request.method == "POST":
        data = request.get_json()

        user_id = get_jwt_identity()
        content = data["content"]
        static_file = data["static_file"]
        status = data["status"]
        if not content and not static_file:
            return jsonify({"Fail"})
        sql = '''
        INSERT INTO article(user_id,content,static_file,publish_time,status)
        VALUES(%s,%s,%s,NOW(),%s)
        '''
        values = (user_id,content,static_file,status, )
        query_CUD(sql, values)
        return jsonify({"Message": "Post successfully!!!"}),200

@posts.route("/api/update-post/<int:id>", methods = ["PUT"])
@jwt_required()
def update_post(id=None):
    if request.method == "PUT":
        if id:
            data = request.get_json()

            content = data["content"]
            static_file = data["static_file"]
            status = data["status"]

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

@posts.route("/api/sreach", methods = ["GET"])
@jwt_required()
def sreach():
        key = request.args.get('keyword', '')
        sql = f'''
        SELECT * FROM user WHERE public_name LIKE "%{key}%" and user_id != "{get_jwt_identity()}"
        '''
        users = query_select(sql)
        if not users:
            return jsonify("")
        res = []
        for user in users:
            res.append({
                'public_name' : user[1],
                'phone': user[4],
                'avatar' : user[2],
            })
        return jsonify({"users": res}), 200
