from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()
DEFAULT_IMG_URL = "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.zelda.com%2Flinks-awakening%2F&psig=AOvVaw09tjltRNWVspEv0G6wfyNo&ust=1678644439567000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCLj3roG81P0CFQAAAAAdAAAAABAJ"

class User(db.Model):
    """Users"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMG_URL)

    posts = db.relationship('Post', backref='user', cascade='all, delete-orphan')

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
class Post(db.Model):
    """User Posts"""
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
class Tag(db.Model):
    """Tags"""
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship("Post", secondary='posts_tags', backref='tags')

class PostTag(db.Model):
    """reference tags ON posts"""
    __tablename__ = "posts_tags"

    tags_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    posts_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)





def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()
