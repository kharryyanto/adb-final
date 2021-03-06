import json
import os
from neo4j import GraphDatabase, basic_auth
from courses import add_course, create_course_levels
from languages import add_language
from provider import add_provider
from knowledge import add_knowledge
from weekSection import add_weekSection
from authors import add_author
from helpers import clear_db
from add_course_weeks_section import add_course_weeks_section
from add_course_lang import add_course_lang
from add_course_keywords import add_course_keywords
from add_course_provider import add_course_provider
from add_course_authors import add_course_authors
from courses_required_prerequisites import create_prerequisites_and_required
from user_history import seed_user_history
from users import create_users

file = open('data/adb_courses.json', "rb", buffering=0)
data = json.load(file)


# Publish in heroku
graphenedb_url = os.environ.get("GRAPHENEDB_BOLT_URL")
graphenedb_user = os.environ.get("GRAPHENEDB_BOLT_USER")
graphenedb_pass = os.environ.get("GRAPHENEDB_BOLT_PASSWORD")

# for running in local computer
if not graphenedb_url or graphenedb_url == '':
    graphenedb_url = 'bolt://localhost:7687'
if not graphenedb_user or graphenedb_user == '':
    graphenedb_user = 'neo4j'
if not graphenedb_pass or graphenedb_pass == '':
    graphenedb_pass = 'password'

# Link the app to the Flask database
driver = GraphDatabase.driver(
    graphenedb_url, auth=basic_auth(graphenedb_user, graphenedb_pass))


def seed_data(driver):
    # Set up database connection
    session = driver.session()

    # Misc
    create_course_levels(driver)

    # We start with the courses basic information
    for _, course in enumerate(data['Title'].items()):
        course = add_course(driver, course[0])

    language = add_language(driver)
    providers = add_provider(driver)
    tags = add_knowledge(driver)
    week = add_weekSection(driver)
    authors = add_author(driver)

    # Add relationships to seed
    add_course_weeks_section(driver)
    add_course_lang(driver)
    add_course_keywords(driver)
    add_course_provider(driver)
    add_course_authors(driver)

    create_prerequisites_and_required(driver)
    create_users(driver)

    seed_user_history(driver)


seed_data(driver)
