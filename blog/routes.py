from flask import Flask, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required

from blog import app, db, bcrypt
from blog.models import User, Post, user_schema, users_schema, post_schema, posts_schema

from .chest import predict


@app.route('/api/users/register', methods=['POST'])
def register():
    username = request.get_json()['username']
    email = request.get_json()['email']
    password = request.get_json()['password']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    user = User(
        username=username,
        email=email,
        password=hashed_password
    )
    db.session.add(user)
    db.session.commit()
    print(user)
    result = {
        'username': user.username,
        'email': user.email,
        'image': user.image_file,
        'created': user.created
    }
    print(jsonify(result))
    return user_schema.dump(user)


@app.route('/api/users/login', methods=['POST'])
def login():
    email = request.get_json()['email']
    password = request.get_json()['password']
    result = jsonify({
        "Error": "Can't login"
    })
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user, remember=bool(request.get_json()['remember']))
        print(user)
        result = {
            'username': user.username,
            'email': user.email,
            'image': user.image_file,
            'created': user.created
        }
        print(jsonify(result))
        result = user_schema.dump(user)
    return result


@app.route('/api/user', methods=['GET'])
@login_required
def get_user():
    print(current_user)
    user = user_schema.dump(current_user)
    return jsonify({
        'status': 'Done',
        'user': user
    })


@app.route('/api/users')
@login_required
def get_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users))


@app.route('/api/users/logout')
def logout():
    logout_user()
    return jsonify({
        "status": "logout"
    })


@app.route('/api/posts/new/ray', methods=['POST'])
@login_required
def add_post():
    image = request.get_json()['image']
    post = Post(
        title=predict(image),
        content=image,
        author=current_user
    )
    db.session.add(post)
    db.session.commit()
    result = jsonify({
        'title': post.title,
        'contetn': post.content,
        'author_id': post.author.id
    })
    return post_schema.dump(post)


@app.route('/api/posts')
@login_required
def get_posts():
    posts = Post.query.all()
    return jsonify(posts_schema.dump(posts))


@app.route('/api/posts/<int:id>')
@login_required
def get_post(id):
    post = Post.query.get(id)
    if post:
        print(post)
        result = {
            "title": post.title,
            "content": post.content,
            "date_posted": post.date_posted,
            "author_id": post.author.id
        }
        print(jsonify(result))
        return post_schema.dump(post)
    return jsonify({
        'status': False,
        "message": "Post not found"
    })


@app.route('/api/posts/<int:id>', methods=['DELETE'])
@login_required
def delete_post(id):
    post = Post.query.get(id)
    result = {
        "STATUS": "DELETED FAILED"
    }
    if post:
        db.session.delete(post)
        db.session.commit()
        result = {
            "STATUS": "DELETED DONE"
        }
    return jsonify(result)
