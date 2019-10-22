from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

from myblog.models import Post
from myblog.post.form import PostForm
from myblog import db


posts = Blueprint("posts", __name__)


@posts.route('/')
def index():
    posts = Post.query.order_by(Post.last_modified.desc()).all()

    return render_template('post/index.html', posts=posts)


@posts.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            body=form.body.data,
            user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts.index'))
    return render_template('post/create-post.html', form=form)


@posts.route("/post/<int:post_id>")
def detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post/detail.html', post=post)
