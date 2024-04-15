#!/usr/bin/python3
""" Guidy Blueprint """

from flask import *
from uuid import uuid4
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from app_server.blueprints.forms import *
from models import storage as db
from models.course import Course
from models.AI.AI_service import Guidy

auth = Blueprint('auth', __name__)
Manager = LoginManager()


@Manager.user_loader
def load_user(user_id):
    """ Load user """
    return db.session.query(User).get(user_id)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """ Landing page route handler"""
    form = LoginForm()
    if current_user.is_authenticated:
        flash('You are already logged in!')
        # get_flashed_messages()
        # return redirect(url_for('auth.profile', userid=current_user.id))

    if request.method == 'POST' and form.validate_on_submit():
        identity = form.username.data
        password = form.password.data

        if '@' in identity and '.' in identity and identity[-1] != '.':
            user = db.session.query(User).filter_by(email=identity).first()
        else:
            user = db.session.query(User).filter_by(username=identity).first()

        if user is not None and user.check_password(password):
            login_user(user)
            user.authenticated = True
            db.session.add(user)
            db.save()
            return "Logged in successfully!"
            # return redirect(url_for('profile', username=user.username))
        else:
            flash(f'{field}: {error}' for field, error in form.errors.items())

    return render_template('login.html', form=form)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """ Register page route handler"""
    form = RegisterForm()
    if form.validate_on_submit() and request.method == 'POST':
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        user = User(username=username, email=email,
                    first_name=first_name, last_name=last_name,
                    password=password)
        db.session.add(user)
        db.save()
        flash(f'User {user.username} created successfully!')
        return redirect(url_for('auth.login', cache_id=uuid4()))
    else:
        for field, error in form.errors.items():
            for err in error:
                flash(f'{field}: {err}')
    return render_template('signup.html', form=form,
                           cache_id=uuid4())

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    """ Logout page route handler"""
    user = current_user
    user.authenticated = False
    session.add(user)
    db.save()
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/profile/<username>', methods=['GET'])
@login_required
def profile():
    """ Profile page route handler"""
    user = current_user()
    username = user.username
    return render_template('dashboard.html', user=user,
                           courses=user.courses)

@auth.route('/profile/<username>/update', methods=['GET', 'POST'])
@login_required
def update(username):
    """ Profile page route handler"""
    form = ProfileForm()
    user = current_user()
    username = user.username
    courses = user.courses
    return render_template('profile.html', user=user, courses=courses, form=form)

@auth.route('/<username>/<coursename>', methods=['GET'])
@login_required
def course(username, course):
    """ Course page route handler"""
    user = current_user()
    course = db.session.query(Course).filter_by(name=course).first()
    return render_template('course.html', user=user, course=course)

@auth.route('/<username>/create', methods=['GET', 'POST'])
@login_required
def create(username):
    """ Course page route handler"""
    form = CourseForm()
    user = current_user()
    if form.validate_on_submit() and request.method == 'POST':
        subject = form.subject.data
        categorey = form.category.data
        resource_type = form.resource_type.data
        level = form.course_level.data
        number_of_lessons = form.number_of_lessons.data
        course = Guidy.CreateCourse(subject, level, number_of_lessons)
        generated_course = Course(name=course['title'],
                                  category=course['category'],
                                  description=course['description'],
                                  level=course['level'],
                                  number_of_lessons=course['length'],
                                  resource_type=resource_type,
                                  lessons_titles=course['lessons_titles'])
        db.session.add(generated_course)
        user.courses.append(generated_course)
        db.save()
        return redirect(url_for('auth.course', username=username,
                                coursename=generated_course.name))
    return render_template('create.html', form=form)
