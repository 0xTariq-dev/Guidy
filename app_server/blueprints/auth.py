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
        # get_flashed_messages()
        return redirect(url_for('auth.dashboard'))
        

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
            return redirect(url_for('auth.dashboard'))
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

@auth.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """ Profile page route handler"""
    form = ProfileForm()
    user = current_user
    if request.method == 'POST':
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        session.add(user)
        db.save()
        flash(f'User {user.username} updated successfully!')
        return render_template('account.html', user=user, form=form)
    else:
        for field, error in form.errors.items():
            for err in error:
                flash(f'{field}: {err}')

    return render_template('account.html', user=user, form=form)



@auth.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """ dashboard page route handler"""
    user = current_user
    print(user)
    print(user.courses)
    return render_template('dashboard.html', user=user, courses=user.courses)

@auth.route('/courses/<coursename>/<course_id>', methods=['GET'])
@login_required
def course(coursename, course_id):
    """ Course page route handler"""
    user = current_user
    courses = [course for course in user.courses if course.id == course_id]
    course = courses[0]
    lessons = course.lessons_titles.replace("'", "\"")
    lessons = json.loads(lessons)
    return render_template('courses.html', course=course, lessons=lessons)

@auth.route('/new_course', methods=['GET', 'POST'])
@login_required
def new_course():
    """ Course page route handler"""
    form = CourseForm()
    user = current_user

    if request.method == 'POST':
        subject = form.title.data
        categorey = form.category.data
        resource_type = form.resource_type.data
        level = form.level.data
        number_of_lessons = form.length.data
        print("Hello from new course")
        course = Guidy.CreateCourse(subject, level, number_of_lessons)
        generated_course = Course(title=course['title'],
                                  category=course['category'],
                                  description=course['description'],
                                  level=course['level'],
                                  length=course['length'],
                                  resource_type=resource_type,
                                  lessons_titles=course['lessons'])
        db.session.add(generated_course)
        user.courses.append(generated_course)
        db.save()
        # return redirect(url_for('auth.course', username=username,
        #                         coursename=generated_course.name))
    return render_template('new_course.html', form=form)
