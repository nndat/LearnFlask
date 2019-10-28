from flask import (Blueprint, render_template, redirect, flash,
                   url_for, request, abort)
from flask_login import current_user, login_required

from myblog.models import Post, Tag, Comment
from myblog.post.form import PostForm
from myblog import db


posts = Blueprint("posts", __name__)


def gettags(s):
    tags = []
    if len(s.strip()) > 0:
        for name in s.split(','):
            name = name.strip()
            tag = Tag.query.filter(Tag.name == name).first()
            if tag is None:
                tag = Tag(name=name)
            tags.append(tag)
    return tags


@posts.route('/')
def index():
    posts = Post.query.order_by(Post.last_modified.desc()).all()

    return render_template('post/index.html', posts=posts)


@posts.route('/tags')
def tags():
    tags = Tag.query.all()
    return render_template('post/tags.html', tags=tags)


@posts.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data.capitalize(),
            body=form.body.data,
            user_id=current_user.id,
            tags=gettags(form.tags.data)
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts.index'))
    return render_template('post/create-post.html', form=form)


@posts.route("/post/<int:post_id>")
def detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post/detail.html', post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data.capitalize()
        post.body = form.body.data
        post.tags = gettags(form.tags.data)
        db.session.commit()
        flash("You post have been updated", "success")
        return redirect(url_for('posts.detail', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body
        form.tags.data = ', '.join([tag.name for tag in post.tags])
    return render_template('post/update-post.html', form=form)


@posts.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = post.tags.all()
    if post.author != current_user:
        abort(403)
    for comment in post.comments:
        db.session.delete(comment)
    db.session.delete(post)
    for tag in tags:
        if len(tag.posts) == 0:
            db.session.delete(tag)
    db.session.commit()
    flash("Your post have been deleted success", "success")
    return redirect(url_for('posts.index'))


@posts.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        keyword = request.form.get('search')
        posts = Post.query.filter(Post.title.contains(keyword)
                                  | Post.body.contains(keyword)).all()
        return render_template('post/search.html',
                               posts=posts, keyword=keyword)
    else:
        return redirect(url_for('posts.index'))


@posts.route('/comment/<int:post_id>', methods=['POST', 'GET'])
@login_required
def comment(post_id):
    if request.method == 'POST':
        content = request.form.get('content')
        comment = Comment(
            body=content,
            post_id=post_id,
            user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for('posts.detail', post_id=post_id))


@posts.route('/delete_comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    cm = Comment.query.get_or_404(comment_id)
    if cm and cm.author == current_user:
        post_id = cm.post_id
        db.session.delete(cm)
        db.session.commit()
        return redirect(url_for('posts.detail', post_id=post_id))
