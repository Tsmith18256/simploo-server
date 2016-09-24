from flask import jsonify

from . import main


@main.route('/', methods=['GET'])
def index():
    return jsonify({
        'success': True
    })
