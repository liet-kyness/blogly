from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db,  User, Post, Tag, PostTag

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
    tags = Tag.query.all()
    return render_template('/posts/new.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_post(user_id):
    user = User.query.get(user_id)
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post(title=request.form['title'], 
                    content=request.form['content'],
                    user=user, tags=tags)
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
    tags = Tag.query.all()
    return render_template('/posts/edit.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_post(post_id):
    post = Post.query.get(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

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

##TAGS#######################################################################

@app.route('/tags')
def tags_all():
    tags = Tag.query.all()

    return render_template("/tags/index.html", tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_info(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('/tags/show.html', tag=tag)

@app.route('/tags/new')
def new_tag_form():
    posts = Post.query.all()
    return render_template('/tags/new.html', posts=posts)

@app.route('/tags/new', methods=['POST'])
def create_new_tag():
    post_ids = [int(num) for num in request.form.getlist('posts')]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(tag_name=request.form['tag_name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    flash(f"{new_tag} added.")
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    tag = Tag.query.get(tag_id)
    posts = Post.query.all()

    return render_template('/tags/edit.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def update_tag(tag_id):
    tag = Tag.query.get(tag_id)
    tag.tag_name = request.form['tag_name']
    post_ids = [int(num) for num in request.form.getlist('posts')]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"{tag.tag_name} updated.")

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)

    db.session.delete(tag)
    db.session.commit()

    flash(f"{tag.tag_name} deleted")

    return redirect('/tags')