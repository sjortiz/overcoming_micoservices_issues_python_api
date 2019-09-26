# Third-party dependencies
from bson.objectid import ObjectId
# Custom dependencies
from .connections import cache


class Todo:

    def __init__(self, collection):
        self.collection = collection

    def get_with_id(self, todo_id):

        key = __name__ + 'todo' + todo_id
        cached_data = cache.fetch(key)

        if cached_data:
            return cached_data

        data = self.collection.find_one({'_id': ObjectId(todo_id)})

        if data:
            data.update({'_id': str(data['_id'])})

        cache.add(key, data)

        return data or {}  # Returns empty dict if data doesn't exist
