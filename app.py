from flask import Flask, request, Response
import json

from controllers.db import LinksController
from controllers.response import send_failed, send_success

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









if __name__ == '__main__':
    app.run(debug=True, port=7003)