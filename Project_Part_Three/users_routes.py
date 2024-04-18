from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import db, User, Post, Tag, PostTag
from datetime import datetime

users_bp = Blueprint('users', __name__, url_prefix='/users')
posts_bp = Blueprint('posts', __name__, url_prefix='/posts')
tags_bp = Blueprint('tags', __name__, url_prefix='/tags')

# Routes for Users
@users_bp.route('/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('show.html', user=user)

@users_bp.route('/<int:user_id>/posts/new', methods=['GET'])
def show_add_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('new_post.html', user=user)

@users_bp.route('/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']

    if not title or not content:
        flash('Title and content are required.', 'error')
        return redirect(url_for('users.show_add_post_form', user_id=user_id))

    new_post = Post(title=title, content=content, created_at=datetime.utcnow(), user_id=user.id)
    db.session.add(new_post)
    db.session.commit()
    flash('Post added successfully!', 'success')

    return redirect(url_for('users.show_user', user_id=user_id))

# Routes for Tags
@tags_bp.route('/')
def list_tags():
    tags = Tag.query.all()
    return render_template('tags/list.html', tags=tags)

@tags_bp.route('/new', methods=['GET'])
def show_add_tag_form():
    return render_template('tags/new.html')

@tags_bp.route('/new', methods=['POST'])
def add_tag():
    name = request.form['name']

    if not name:
        flash('Tag name is required.', 'error')
        return redirect(url_for('tags.show_add_tag_form'))

    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    flash('Tag added successfully!', 'success')

    return redirect(url_for('tags.list_tags'))

# Additional Tag Routes (edit, delete, etc.)...

# Routes for Posts (with tagging functionality)
@posts_bp.route('/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

@posts_bp.route('/<int:post_id>/edit', methods=['GET'])
def show_edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)

@posts_bp.route('/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    title = request.form['title']
    content = request.form['content']

    if not title or not content:
        flash('Title and content are required.', 'error')
        return redirect(url_for('posts.show_edit_post_form', post_id=post_id))

    post.title = title
    post.content = content
    db.session.commit()
    flash('Post updated successfully!', 'success')

    return redirect(url_for('posts.show_post', post_id=post_id))

@posts_bp.route('/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')

    return redirect(url_for('users.show_user', user_id=post.user_id))
