from myblog import db
from flask_login import UserMixin

from datetime import datetime


def slugtify(s):
    return '-'.join([w.strip() for w in s.split()])


posts_tags = db.Table(
    "posts_tags",
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    def __repr__(self):
        return f"<User: {self.username}>"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_modified = db.Column(db.DateTime, default=datetime.now,
                              onupdate=datetime.now)
    tags = db.relationship(
        "Tag",
        secondary=posts_tags,
        backref="posts",
        lazy="dynamic"
    )

    comments = db.relationship('Comment', backref="post", lazy=True)

    def generate_slug(self):
        self.slug = ''
        if self.title:
            self.slug = slugtify(self.title)

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    def __repr__(self):
        return f'<Post {self.title}>'


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False)

    def generate_slug(self):
        self.slug = ''
        if self.name:
            self.slug = slugtify(self.name)

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.generate_slug()

    def __repr__(self):
        return f"<Tag {self.name}>"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, default=datetime.now)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f'<Comment body>'
