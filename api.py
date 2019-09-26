from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
tasks = []


class Todos(Resource):
    def get(self, todo_id=None):
        return tasks

    def post(self):
        tasks.append({'task': len(tasks)+1})


class TodoItem(Resource):

    def get(self, todo_id):
        for x in tasks:
            if x['task'] == todo_id:
                return x

        return {}


api.add_resource(Todos, '/')
api.add_resource(TodoItem, '/id/<int:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
