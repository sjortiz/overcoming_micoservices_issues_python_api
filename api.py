import time
from pymongo import MongoClient
from flask import Flask, request
from flask_restful import Resource, Api
from bson.objectid import ObjectId
from redis import StrictRedis
from redis_cache import RedisCache

# Flask configuration
app = Flask(__name__)
api = Api(app)
# Mongo configuration
client = MongoClient(
            host="0.0.0.0",
            port=27017,
            username="root",  # <- Credentials manager
            password="toor",  # <- Credentials manager
        )
db = client['todos']
collection = db['tasks']
# Redis cache configuraiton
client = StrictRedis(host="0.0.0.0", port=6379, db=0, decode_responses=True)
cache = RedisCache(redis_client=client)


# Separating the get_with_id function from the endpoint
@cache.cache(ttl=5)
def get_with_id(todo_id):

    time.sleep(5)
    data = collection.find_one({'_id': ObjectId(todo_id)})

    if data:
        data.update({'_id': str(data['_id'])})

    return (data or {})


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
        return get_with_id(todo_id)


api.add_resource(Todos, '/')
api.add_resource(TodoItem, '/id/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
