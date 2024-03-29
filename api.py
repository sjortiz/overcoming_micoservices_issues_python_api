# Third-party libraries
from pymongo import MongoClient
from flask import Flask, request
from flask_restful import Resource, Api
# Custom libraries
from resources.todo import Todo
from resources.connections import credentials
# Instanciating mongo credentials
mongo_credentials = credentials.get_credentials('mongo_credentials')

# Flask configuration
app = Flask(__name__)
api = Api(app)
# Mongo configuration
client = MongoClient(
            host="mongo",
            port=27017,
            username=mongo_credentials.get('mongo_user'),
            password=mongo_credentials.get('mongo_password'),
        )
db = client['todos']
collection = db['tasks']
todo = Todo(collection)


class Todos(Resource):

    def get(self):
        return [
            {
                **task,
                **{'_id': str(task['_id'])}
            }
            for task in collection.find({})
        ]

    def post(self):

        data = request.get_json().get('task')

        if data:
            task_id = collection.insert_one({
                'task': data
            })

            return {'ID': str(task_id.inserted_id)}

        return {}


class TodoItem(Resource):

    def get(self, todo_id):
        return todo.get_with_id(todo_id)


api.add_resource(Todos, '/')
api.add_resource(TodoItem, '/id/<string:todo_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
