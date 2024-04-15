#!/usr/bin/python3
"""Login Form"""

import re
from models import storage as db
from models.user import User
# from models.course import Course
# from models.lesson import Lesson
# from models.resource import Resource
# from models.review import Review
# from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo

session = db.session

class LoginForm(FlaskForm):
    username = StringField(id='username', name='username or email',
                           validators=[InputRequired()],
                           render_kw={'placeholder': 'Username or Email'}
                           )
    password = PasswordField(id='password', name='password',
                             validators=[InputRequired()],
                             render_kw={'placeholder': 'Password'}
                             )
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
    def validate_username(self, username):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        username_regex = r'^[a-zA-Z0-9_.-]+$'
        username = username.data

        if re.match(email_regex, username):
            return 'email'
        elif re.match(username_regex, username):
            return 'username'
        else:
            return None

class RegisterForm(FlaskForm):
    first_name = StringField(id='first name', name='First name',
                             validators=[InputRequired(),
                                         Length(min=2, max=60)],
                             render_kw={'placeholder': 'First Name'}
                            )
    last_name = StringField(id='last name', name='Last name',
                            validators=[InputRequired(),
                                        Length(min=2, max=60)],
                            render_kw={'placeholder': 'Last Name'}
                            )
    username = StringField(id='username', name='Username',
                           validators=[InputRequired(),
                                       Length(min=4, max=20)],
                           render_kw={'placeholder': 'Username'}
                           )
    email = StringField(id='email', name='Email',
                        validators=[InputRequired(), Email(),
                                    Length(min=6, max=60)],
                        render_kw={'placeholder': 'Email'}
                        )
    password = PasswordField(id='password', name='Password',
                             validators=[InputRequired(),
                                         Length(min=8, max=20)],
                             render_kw={'placeholder': 'Password'}
                             )
    confirm_password = PasswordField(id='confirm password', name='Confirm Password',
                                     validators=[InputRequired(),
                                                 EqualTo('password', message='Passwords must match')],
                                     render_kw={'placeholder': 'Confirm Password'})
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        username_regex = r'^[a-zA-Z0-9_.-]+$'
        user = session.query(User).filter_by(username=username.data).first()
        username = username.data

        if user:
            raise ValidationError('Username already exists, please choose another one.')

        if re.match(username_regex, username):
            return True
        else:
            raise ValidationError('Username must contain only alphanumeric characters, dots, underscores, and hyphens.')

    def validate_email(self, email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        user = session.query(User).filter_by(email=email.data).first()
        email = email.data
        
        if user:
            raise ValidationError('Email already registered, Login instead.')
        if re.match(email_regex, email):
            return True
        else:
            raise ValidationError('Invalid email address.')

    def validate_password(self, password):
        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d.]{8,}$'
        password = password.data

        if re.match(password_regex, password):
            return True
        else:
            raise ValidationError('Password must contain at least one lowercase letter, one uppercase letter, one digit, and be at least 8 characters long.')

class ProfileForm(FlaskForm):
    """Profile Form"""
    first_name = StringField(id='first name', name='First name',
                             validators=[InputRequired(),
                                         Length(min=2, max=60)],
                             render_kw={'placeholder': 'First Name'}
                            )
    last_name = StringField(id='last name', name='Last name',
                            validators=[InputRequired(),
                                        Length(min=2, max=60)],
                            render_kw={'placeholder': 'Last Name'}
                            )
    email = StringField(id='email', name='Email',
                        validators=[InputRequired(), Email(),
                                    Length(min=6, max=60)],
                        render_kw={'placeholder': 'Email'}
                        )
    submit = SubmitField('Update')

    def validate_username(self, username):
        username_regex = r'^[a-zA-Z0-9_.-]+$'
        
        if re.match(username_regex, username):
            return 'username'
        else:
            return None

    def validate_email(self, email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        if re.match(email_regex, email):
            return 'email'
        else:
            return None

    def validate_password(self, field):
        password = field.data
        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$'
        
        if re.match(password_regex, password):
            return 'password'
        else:
            return None

class CourseForm(FlaskForm):
    title = StringField(id='title', name='Title',
                        validators=[InputRequired(),
                                    Length(min=4, max=128)],
                        render_kw={'placeholder': 'Title'}
                        )
    category = StringField(id='category', name='Category',
                           validators=[InputRequired(),
                                       Length(min=4, max=128)],
                           render_kw={'placeholder': 'Category'}
                           )
    description = StringField(id='description', name='Description',
                              validators=[InputRequired(),
                                          Length(min=4, max=1024)],
                              render_kw={'placeholder': 'Description'}
                              )
    length = StringField(id='length', name='Length',
                         validators=[InputRequired()],
                         render_kw={'placeholder': 'Length'}
                         )
    level = StringField(id='level', name='Level',
                        validators=[InputRequired(),
                                    Length(min=4, max=60)],
                        render_kw={'placeholder': 'Level'}
                        )
    resource_type = SelectField(id='resource_type', name='Resource Type',
                                validators=[InputRequired(),
                                            Length(min=4, max=60)],
                                render_kw={'placeholder': 'Resource Type'},
                                choices=[('video', 'Videos'), ('articles', 'Articles'),
                                         ('doc', 'Documentations'), ('tutorial', 'Tutorials')]
                                )
    submit = SubmitField('Create Course')
