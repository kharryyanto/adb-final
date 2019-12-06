import json
from neo4j import GraphDatabase, basic_auth

# Load and parse data
file = open('data/adb_courses.json', "rb", buffering=0)
data = json.load(file)

# Create graph driver
# This is used to create a session so we can run the code while working on it.
driver = GraphDatabase.driver('bolt://localhost:7687',
                              auth=basic_auth('neo4j',  'password'))


def add_language(driver):
    """Add the languages to the database"""
    # Create session
    session = driver.session()

    # Get unique languages
    languages = list(set(data['Language'].values()))

    # Create language nodes
    for language in languages:
        session.run(
            'CREATE (l:Language {language: $language }) RETURN l', language=language)

    session.close()

    return languages


print('Languages added were: ', add_language(driver))