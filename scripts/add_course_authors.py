import json
from neo4j import GraphDatabase, basic_auth
from helpers import get_connection_details

# Load and parse data
file = open('data/adb_courses.json', "rb", buffering=0)
data = json.load(file)

graphenedb_url = get_connection_details()[0]
graphenedb_user = get_connection_details()[1]
graphenedb_pass = get_connection_details()[2]

# Create graph driver
# This is used to create a session so we can run the code while working on it.
driver = GraphDatabase.driver(graphenedb_url,
                              auth=basic_auth(graphenedb_user, graphenedb_pass))


def add_course_authors(driver):
    session = driver.session()
    for course in data['Title'].items():
        course_id = course[0]
        course_authors_list = data['Author'][course_id]

        if type(course_authors_list) is list:
            if course_authors_list:
                for author in course_authors_list:
                    if author != '':
                        session.run(
                            'MATCH (a:Author), (c:Course) WHERE c.course_id = $course_id AND a.author = $author CREATE (a)-[r:TEACHES]->(c) RETURN type(r)', course_id=course_id, author=author)
        else:
            if course_authors_list != '':
                session.run(
                    'MATCH (a:Author), (c:Course) WHERE c.course_id = $course_id AND a.author = $course_authors_list CREATE (a)-[r:TEACHES]->(c) RETURN type(r)', course_id=course_id, course_authors_list=course_authors_list)
    session.close()
    return 'Author-Course Relationship created.'


if __name__ == '__main__':
    print(add_course_authors(driver))
