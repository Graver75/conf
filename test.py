import unittest, redis, requests, json
from datetime import datetime


POST_URL = 'http://localhost:7003/visited_links'
GET_URL = 'http://localhost:7003/visited_domains'

TEST_DATA_1 = {
    "links": [
        "https://ya.ru",
        "https://ya.ru?q=123",
        "funbox.ru",
        "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor",
        "vk.com"
    ]
}
TEST_DATA_2 = {
    "links": [
        "vk.com",
        "google.ru",
        "yandex.ru",
        "ok.ru",
        "bing.com",
        "kk.ru",
        "foo.bar"
    ]
}
WRONG_TEST_DATA = 'beleberda'

SUCCESS_STATUS_CODE = 200
FAILED_STATUS_CODE = 400

r = redis.Redis(host='localhost', port=6379, db=0)


def get_time():
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    return int((now - epoch).total_seconds())


def http_post(body):
    return requests.post(POST_URL, json=body)


def http_get(from_arg, to_arg):
    return requests.get(GET_URL, params={'from': from_arg, 'to': to_arg})



class AppTest(unittest.TestCase):
    # simple tests
    def test1_empty_post(self):
        result = http_post({})
        status = json.loads(result.content)['status']
        self.assertEqual(status, "KeyError")

    def test2_base_post(self):
        result = http_post(TEST_DATA_1)
        self.assertEqual(result.status_code, 200)

        result = http_post(WRONG_TEST_DATA)
        status = json.loads(result.content)['status']
        self.assertEqual(status, "TypeError")

    def test3_empty_get(self):
        result = http_get(0, 0)
        self.assertEqual(result.status_code, 200)

    def test4_base_get(self):
        time_a = 0
        time_b = 2000000000

        result = http_get(time_a, time_b)
        links = json.loads(result.content)['links']
        self.assertIn('ya.ru', links)
        self.assertIn('vk.com', links)

    def test5_compex_get(self):
        # check duplicates
        http_post(TEST_DATA_2)
        time_a = 0
        time_b = 2000000000

        result = http_get(time_a, time_b)
        links = json.loads(result.content)['links']
        links.remove('vk.com')
        self.assertNotIn('vk.com', links)

