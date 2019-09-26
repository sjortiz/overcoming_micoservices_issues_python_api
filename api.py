from pymongo import MongoClient
from flask import Flask, request
from flask_restful import Resource, Api
from bson.objectid import ObjectId

app = Flask(__name__)
api = Api(app)
client = MongoClient(
            host="0.0.0.0",
            port=27017,
            username="root",
            password="toor",
        )
db = client['todos']
collection = db['tasks']


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
        data = collection.find_one({'_id': ObjectId(todo_id)})

        if data:
            data.update({'_id': str(data['_id'])})

        return data or {}


api.add_resource(Todos, '/')
api.add_resource(TodoItem, '/id/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
