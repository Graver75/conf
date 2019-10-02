from flask import Flask, request
import json

from controllers.db import LinksController
from controllers.response import send_failed, send_success, send_body_success

app = Flask(__name__)
links_controller = LinksController()


@app.route('/visited_links', methods=["POST"])
def post_links():
    try:
        links = json.loads(request.data)['links']
        links_controller.post(links)
    except Exception as e:
        return send_failed(e)
    else:
        return send_success()


@app.route('/visited_domains', methods=["GET"])
def get_links():
    from_arg = int(request.args.get('from'))
    to_arg = int(request.args.get('to'))

    links = links_controller.get(from_arg, to_arg)
    return send_body_success(links)


if __name__ == '__main__':
    app.run(debug=True, port=7003)