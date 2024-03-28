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
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is None:
            return
        
        if isinstance(obj, User):
            self.__delete_user(obj)
            return

        if isinstance(obj, Course):
            self.__delete_course(obj)
            return

        if isinstance(obj, Lesson):
            self.__delete_lesson(obj)
            return

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

    def __delete_user(self, user):
        """delete user and associated objects"""
        courses = self.__session.query(Course).filter(Course.user_id == user.id).all()
        for course in courses:
            lessons = self.__session.query(Lesson).filter(Lesson.course_id == course.id).all()
            for lesson in lessons:
                resources = self.__session.query(Resource).filter(Resource.lesson_id == lesson.id).all()
                [self.__session.delete(resource) for resource in resources]
                self.__session.delete(lesson)
            reviews = self.__session.query(Review).filter(Review.course_id == course.id).all()
            [self.__session.delete(review) for review in reviews]
            self.__session.delete(course)
        self.__session.flush()
        self.__session.delete(user)
        self.save()

    def __delete_course(self, course):
        """delete course and associated objects"""
        lessons = self.__session.query(Lesson).filter(Lesson.course_id == course.id).all()
        for lesson in lessons:
            resources = self.__session.query(Resource).filter(Resource.lesson_id == lesson.id).all()
            [self.__session.delete(resource) for resource in resources]
            self.__session.delete(lesson)
        reviews = self.__session.query(Review).filter(Review.course_id == course.id).all()
        [self.__session.delete(review) for review in reviews]
        self.__session.flush()
        self.__session.delete(course)
        self.save()

    def __delete_lesson(self, lesson):
        """delete lesson and associated objects"""
        resources = self.__session.query(Resource).filter(Resource.lesson_id == lesson.id).all()
        [self.__session.delete(resource) for resource in resources]
        self.__session.delete(lesson)
        self.__session.flush()
        self.save()
