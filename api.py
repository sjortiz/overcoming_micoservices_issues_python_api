from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

tasks = []

class Todo(Resource):
    def get(self):
            return tasks
    
    def post(self):
        tasks.append({'task': len(tasks)+1})

api.add_resource(Todo, '/')

if __name__ == '__main__':
    app.run(debug=True)