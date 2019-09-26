from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

tasks = []


class Todo(Resource):
    def get(self, todo_id=None):

        if todo_id:

            for x in tasks:
                if x['task'] == todo_id:
                    return x
            else:
                return {}

        return tasks

    def post(self):
        tasks.append({'task': len(tasks)+1})


api.add_resource(Todo, '/', '/id/<int:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
