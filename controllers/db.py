import redis
from datetime import datetime

r = redis.Redis(host='localhost', port=6379, db=0)


class LinksController():
    def _get_time(self):
        epoch = datetime.utcfromtimestamp(0)
        now = datetime.now()
        return int((now - epoch).total_seconds())

    def post(self, links):
        time = self._get_time()
        for link in links:
            r.rpush(time, link)