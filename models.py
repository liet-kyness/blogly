from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DEFAULT_IMG_URL = "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.zelda.com%2Flinks-awakening%2F&psig=AOvVaw09tjltRNWVspEv0G6wfyNo&ust=1678644439567000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCLj3roG81P0CFQAAAAAdAAAAABAJ"

class User(db.Model):
    """Users"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMG_URL)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()
