from faker import Faker
from random import randint
import uuid
from neo4j import GraphDatabase, basic_auth
from helpers import get_connection_details

graphenedb_url = get_connection_details()[0]
graphenedb_user = get_connection_details()[1]
graphenedb_pass = get_connection_details()[2]

# Create graph driver
# This is used to create a session so we can run the code while working on it.
driver = GraphDatabase.driver(graphenedb_url,
                              auth=basic_auth(graphenedb_user, graphenedb_pass))


class User:
    def __init__(self, id='', username='', name='', age='', university='', password=''):
        self.age = age
        self.id = id
        self.name = name
        self.password = password
        self.university = university
        self.username = username

    def create(self, db):
        user = {
            'age': self.age,
            'id': self.id,
            'name': self.name,
            'password': self.password,
            'university': self.university,
            'username': self.username
        }

        user = db.run('CREATE (u:User $user) RETURN u', user=user)

        return user.value()[0]


# Seed Users
fake = Faker(['en_US'])
universities = ['NTHU', 'NCTU', 'NTU', 'NCCU', 'Stanford', 'Galen']


def create_users(driver):
    db = driver.session()

    for _ in range(250):
        name = fake.name()
        age = randint(15, 55)
        id = str(uuid.uuid4())
        user_name = f"{name.split(' ')[0]}{randint(0, 1000)}"
        university = universities[randint(0, 3)]
        password = 'password'

        User(id=id, username=user_name, name=name,
             age=age, university=university, password=password).create(db)

    db.close()


if __name__ == '__main__':
    create_users(driver)
