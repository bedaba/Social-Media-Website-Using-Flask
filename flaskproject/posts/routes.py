from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flaskproject import db
from flaskproject.models import Post, User
from flaskproject.posts.forms import PostForm

posts = Blueprint('posts', __name__)


#Post page route
@posts.route("/post/new", methods = ['GET','POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title = form.title.data, content = form.content.data, author = current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your post was successfully created', 'success')
		return redirect(url_for('main.home'))
	return render_template('create_post.html', title = 'New Post', form=form, legend = 'New Post')


#Route for specific post id
@posts.route("/post/<int:post_id>")
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post = post)


#Route for post update
@posts.route("/post/<int:post_id>/update", methods = ['GET','POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403) #403 is http response for a forbidden route or url
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('Your post has been successfully updated', 'success')
		return redirect(url_for('posts.post', post_id = post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', title = 'Update Post', form=form, legend = 'Update Post')


#Route for post deletion
@posts.route("/post/<int:post_id>/delete/", methods=['GET','POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

@posts.route('/user/<int:user_id>')
@login_required
def view_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template('user.html', user=user, posts=posts)