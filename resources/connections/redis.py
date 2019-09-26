# built-in dependencies
import json
# Third-party dependencies
from redis import StrictRedis

# Redis cache configuraiton
client = StrictRedis(host="0.0.0.0", port=6379, db=0, decode_responses=True)


class Redis:

    def add(self, key, value) -> None:
        if not isinstance(value, (str, bytes, int)):
            value = json.dumps(value)

        client.set(key, value, ex=5)

    def fetch(self, key) -> dict:
        cached_value = client.get(key)

        if cached_value:
            return json.loads(cached_value)

        return None


cache = Redis()
