import os
import pep8
import inspect
import unittest
from models import storage
from datetime import datetime
from unittest.mock import patch, Mock, MagicMock
from models.engine.db_engine import DBStorage
from models.user import User
from models.course import Course
from models.lesson import Lesson
from models.resource import Resource
from models.review import Review 
from sqlalchemy import create_engine
from os import getenv

classes = {"User": User,
            "Course": Course,
            "Lesson": Lesson,
            "Resource": Resource,
            "Review": Review
            }
    
    
class TestDBStorage(unittest.TestCase):
    @patch('models.engine.db_engine.create_engine')
    @patch('models.engine.db_engine.getenv')
    def test_init(self, mock_getenv, mock_create_engine):
        # Setup the mock values
        mock_getenv.side_effect = ['user', 'password', 'host', 'db', 'test']
        mock_create_engine.return_value = Mock()

        # Instantiate the DBStorage object
        db_storage = DBStorage()

        # Assert that getenv was called with the correct arguments
        mock_getenv.assert_any_call('DBUSER')
        mock_getenv.assert_any_call('PWD')
        mock_getenv.assert_any_call('HOST')
        mock_getenv.assert_any_call('DB')
        mock_getenv.assert_any_call('ENV')

        # Assert that create_engine was called with the correct arguments
        mock_create_engine.assert_called_once_with(
            'mysql+mysqldb://user:password@host/db',
            pool_pre_ping=True
            )

        # Assert that the engine was set correctly
        self.assertIsNotNone(db_storage._DBStorage__engine)

    @patch('models.engine.db_engine.Base.metadata.drop_all')
    @patch('models.engine.db_engine.create_engine')
    @patch('models.engine.db_engine.getenv')
    def test_init_test_env(self, mock_getenv, mock_create_engine, mock_drop_all):
        # Setup the mock values
        mock_getenv.side_effect = ['user', 'password', 'host', 'db', 'test']
        mock_create_engine.return_value = Mock()

        # Instantiate the DBStorage object
        db_storage = DBStorage()

        # Assert that drop_all was called with the correct arguments
        mock_drop_all.assert_called_once_with(db_storage._DBStorage__engine)

if __name__ == '__main__':
    unittest.main()
