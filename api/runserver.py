import os
from flask import Flask, g
from flask_restful import Api
from flask_cors import CORS
from .resources.hello import HelloWorld
from .resources.Author import AuthorResource
from api import app

# Wrap app with API to enable Flask-REST API
api = Api(app)

api.add_resource(AuthorResource, '/authors/<id>')

# Enable debugging mode for dev environments
if __name__ == '__main__':
    app.run(debug=True)
