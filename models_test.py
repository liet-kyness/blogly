from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

with app.app_context():
    db.drop_all()
    db.create_all()


class UserModelTestCase(TestCase):

    def setUp(self):
        User.query.delete()
    
    def tearDown(self):
        db.session.rollback()

    