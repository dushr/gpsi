import unittest
from flask import Flask

from gpsi import app, db
from gpsi.views import *  # noqa


class GPSITests(unittest.TestCase):

    SQLALCHEMY_DATABASE_URI = 'postgres://localhost/gpsi-test'

    fixtures = []

    @classmethod
    def setUpClass(cls):
        """
        Creates a new database for the unit test to use
        """
        app.config['SQLALCHEMY_DATABASE_URI'] = cls.SQLALCHEMY_DATABASE_URI
        db.init_app(app)
        cls.db = db
        with app.app_context():
            db.create_all()
        cls.load_fixtures()
        cls.app = app.test_client()

    @classmethod
    def load_fixtures(cls):
        for fixture in cls.fixtures:
            db.session.add(fixture)
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        """
        Ensures that the database is emptied for next unit test
        """
        cls.app = Flask(__name__)
        db.init_app(cls.app)
        with cls.app.app_context():
            db.drop_all()
