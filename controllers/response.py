from flask import Response, jsonify


def send_success():
    return jsonify({"status": "ok"})


def send_failed(err):
    name = type(err).__name__
    return jsonify({"status": name})