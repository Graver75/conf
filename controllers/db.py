import redis
from urllib.parse import urlparse
from datetime import datetime

r = redis.Redis(host='localhost', port=6379, db=0)


class LinksController():
    def _get_time(self):
        epoch = datetime.utcfromtimestamp(0)
        now = datetime.now()
        return int((now - epoch).total_seconds())

    def _get_all_keys_between(self, a, b):
        return [int(key) for key in r.keys('*') if a <= int(key) <= b]

    def _parse(self, links):
        domains = []
        for link in links:
            # normalising link format for urlparse
            if not 'http' in link:
                link = 'http://' + link

            parsed = urlparse(link)
            domains.append(parsed.hostname)
        return list(set(domains))

    def post(self, links):
        time = self._get_time()
        links = self._parse(links)
        r.sadd(time, *links)

    def get(self, a, b):
        links = []
        keys = self._get_all_keys_between(a, b)
        for key in keys:
            links.append(list(r.smembers(key)))
        links = list(set([item.decode("utf8") for sublist in links for item in sublist]))
        return links
