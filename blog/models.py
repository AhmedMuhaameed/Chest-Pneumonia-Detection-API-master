from datetime import datetime
from flask_login import UserMixin

from blog import db, ma, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.svg')
    password = db.Column(db.String(60), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_type = db.Column(db.String(20), nullable=False, default="Patient")
    posts = db.relationship('Post', backref='author',
                            lazy=True)  # Post refer to class Post

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', {self.email}', {self.image_file}, {self.user_type}', '{self.created}')"


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email',
                  'image_file', 'user_type', 'created', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # user refer to table user and id to id column
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'date_posted', 'content', 'user_id')

    author = ma.Nested(UserSchema)


post_schema = PostSchema()
posts_schema = PostSchema(many=True)
