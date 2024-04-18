#!/usr/bin/env python3
""" Blueprint module """

from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def index():
    """ Landing page route handler"""
    return render_template('index.html')

@views.route('/about')
def about():
    """ About page route handler"""
    return render_template('about.html')

@views.route('/contact')
def contact():
    """ Contact page route handler"""
    return render_template('contact.html')

@views.route('/terms')
def terms():
    """ Terms page route handler"""
    return render_template('terms.html')

@views.route('/privacy')
def privacy():
    """ Privacy page route handler"""
    return render_template('privacy.html')

@views.route('/chat')
def chat():
    """ chat page route handler"""
    return render_template('chat.html')