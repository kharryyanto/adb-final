import os
from flask import Flask, g, Blueprint, render_template, request, redirect, flash, url_for, escape, session
from flask_restful import Api
from flask_cors import CORS
from .resources.Author import AuthorResource
from .resources.Authors import AuthorsResource
from .resources.Courses import CoursesResource
from .resources.Enroll import EnrollResource
from api import app
from py2neo import ogm
from flask2neo4j import Flask2Neo4J
from .resources.forms import CourseSearchForm, SearchForm
from .resources.tables import Results, History, UserResults
#import flask_login

from api.models.course import Course
from api.models.user import User
from api.common.cypher_helpers import page_number, page_size

# Wrap app with API to enable Flask-REST API
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(AuthorsResource, '/authors')
api.add_resource(AuthorResource, '/authors/<int:id>')
api.add_resource(EnrollResource, '/enroll')
# api.add_resource(CoursesResource, '/courses')
app.register_blueprint(api_bp)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# =============================================================================
# login_manager = flask_login.LoginManager()
#
# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)
# =============================================================================


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        flash('Logged in as %s' % escape(session['username']))
        login = True
    else:
        login = False
    search = CourseSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('index.html', form=search, login=login)

# @app.route('/results')


def search_results(search):
    results = []
#    search_dim = search.data['select']
    search_string = search.data['search']

    if search_string == '':
        return render_template('notfound.html')
    else:
        # display results
        results = Course().find(search_string, page_number(), page_size())
        if not results:
            flash(search_string)
            return render_template('notfound.html')
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table, results=results, form=search)

    search = CourseSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('index.html', form=search)

# explore
@app.route('/explore')
def explore():
    return render_template('explore.html')


@app.route('/courses/<id>')
def course_details(id):
    search = CourseSearchForm(request.form)

    course = Course().find_by_id(id)

    enrolled = User().enrolled_in(
        session['username'], id) if 'username' in session else False

    prerequisites = Course().get_prerequisites(id)

    return render_template('course.html', form=search, course=course, enrolled=enrolled)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        login_validation = User().check_password(
            request.form['username'], request.form['password'])
        if not login_validation:
            error = 'Invalid credentials'
        else:
            flash('You were successfully logged in')
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/history')
def history():
    # Use James510 as username for "good" results
    error = None
    try:
        if 'username' in session:
            flash('Logged in as %s' % escape(session['username']))
            login = True
        else:
            login = False

        if session['username']:
            results = User().find_history(
                session['username'], page_number(), page_size())
            table = History(results)
            table.border = True
            return render_template('history.html', error=error, table=table, login=login)
    except:
        error = 'Not logged in'
        return render_template('history.html', error=error)
#    if session['username'] == None:
#        error = 'Not logged in'
#    return render_template('login.html', error=error)


@app.route('/user-search', methods=['GET', 'POST'])
def user():
    if 'username' in session:
        flash('Logged in as %s' % escape(session['username']))
        login = True
    else:
        login = False
    search = SearchForm(request.form)
    if request.method == 'POST':
        return user_search_results(search)
    return render_template('user-search.html', form=search, login=login)

# @app.route('/results')


def user_search_results(search):
    results = []
#    search_dim = search.data['select']
    search_string = search.data['search']

    if search_string == '':
        return render_template('notfound.html')
    else:
        # display results
        results = User().find(search_string, page_number(), page_size())
        if not results:
            flash(search_string)
            return render_template('notfound.html')
        table = UserResults(results)
        table.border = True
        return render_template('user-results.html', table=table, results=results, form=search)

    search = SearchForm(request.form)
    if request.method == 'POST':
        return user_search_results(search)
    return render_template('user-search.html', form=search)


print(app.url_map)

# Enable debugging mode for dev environments
if __name__ == '__main__':
    app.run(debug=True)
