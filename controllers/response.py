from flask import jsonify


def send_success():
    return jsonify({"status": "ok"})


def send_body_success(links):
    return jsonify({
        "links": links,
        "status": "ok"
    })

def send_failed(err):
    name = type(err).__name__
    return jsonify({"status": name})