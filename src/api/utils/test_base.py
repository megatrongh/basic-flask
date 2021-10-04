import unittest2 as unittest
from main import create_app
from api.utils.db import db
from api.config.config import TestingConfig
import tempfile
import os
from sqlalchemy.orm.session import close_all_sessions
from dotenv.main import load_dotenv

load_dotenv()


class BaseTestCase(unittest.TestCase):
    """A base test case"""

    def setUp(self):
        app = create_app(TestingConfig)
        self.test_db_file = tempfile.mkstemp()[1]
        conf_from_env = {**os.environ}
        app.config.update(conf_from_env)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + self.test_db_file

        with app.app_context():
            db.create_all()
        app.app_context().push()
        self.app = app.test_client()

    def tearDown(self):
        close_all_sessions()
        db.drop_all()
