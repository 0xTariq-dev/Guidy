#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
import sqlalchemy
from os import getenv
from models.base_model import BaseModel, Base
from models.user import User
from models.course import Course
from models.lesson import Lesson
from models.resource import Resource
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.session import object_session

classes = {"User": User,
           "Course": Course,
           "Lesson": Lesson,
           "Resource": Resource,
           "Review": Review
           }


class DBStorage:
    """interacts with the MySQL database"""
    __engine = None
    __session = None
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DBStorage, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """Instantiate a DBStorage object"""
        MYSQL_USER = getenv('DBUSER')
        MYSQL_PWD = getenv('PWD')
        MYSQL_HOST = getenv('HOST')
        MYSQL_DB = getenv('DB')
        ENV = getenv('ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(MYSQL_USER,
                                             MYSQL_PWD,
                                             MYSQL_HOST,
                                             MYSQL_DB),
                                      pool_pre_ping=True)

        if ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for cl in classes:
            if cls is None or cls is classes[cl] or cls is cl:
                objs = self.__session.query(classes[cl]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.merge(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is None:
            return
        
        if isinstance(obj, Course):
            lessons = self.__session.query(Lesson).filter(Lesson.course_id == obj.id).all()
            self.__session.delete(lesson for lesson in lessons )
        
        if isinstance(obj, Lesson):
            lessons = self.__session.query(Resource).filter(Resource.lesson_id == obj.id).all()
            self.__session.delete(lesson for lesson in lessons )

        self.__session.delete(obj)
        self.save()

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        create_session = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(create_session)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.close()

    def get(self, cls, id):
        """retrieve one object"""
        if cls is None or cls not in classes.values():
            return None

        all_objs = models.storage.all(cls)
        for val in all_objs.values():
            if val.id == id:
                return val
        return None

    def count(self, cls=None):
        """count the number of objects in storage"""
        all_cls = classes.keys()
        st = models.storage
        count = len(st.all(cls)) if cls else sum(
            [len(st.all(cl)) for cl in all_cls]
            )
        return count
