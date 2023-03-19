from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db,  User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_proj'
app.config['SECRET_KEY'] = 'asdfg124'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True
debug = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()

@app.route('/')
def root():
    posts = Post.query.order_by(Post.created_at.desc()).limit(6).all()
    return render_template('/posts/home.html', posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    render_template('/404.html'), 404




@app.route('/users')
def users_index():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('/users/index.html', users=users)

@app.route('/users/new', methods = ['GET'])
def new_user():
    return render_template('/users/new.html')

@app.route('/users/new', methods = ['POST'])
def create_user():
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url' or None]
    )

    db.session.add(new_user)
    db.session.commit()

    flash(f"New Profile Added! {new_user.full_name}")

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_users(user_id):
    user = User.query.get(user_id)
    return render_template('/users/show.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = User.query.get(user_id)
    return render_template('/users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods = ['POST'])
def update_user(user_id):
    user = User.query.get(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash('Update Successful')

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods = ['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

## POSTS #############################################################################

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    user = User.query.get(user_id)
    return render_template('/posts/new.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_post(user_id):
    user = User.query.get(user_id)
    new_post = Post(title=request.form['title'], 
                    content=request.form['content'],
                    user=user)
    db.session.add(new_post)
    db.session.commit()

    flash(f"{new_post.title} created.")

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_posts(post_id):
    post = Post.query.get(post_id)
    return render_template('/posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get(post_id)
    return render_template('/posts/edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_post(post_id):
    post = Post.query.get(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"{post.title} updated.")

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"{post.title} removed.")

    return redirect('/')
