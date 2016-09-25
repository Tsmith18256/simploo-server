from flask import g, jsonify

from . import users
from .. import auth
from ..models import User


def parse_user(u):
    return {
        'id': u.id,
        'email': u.email,
        'first_name': u.first_name,
        'last_name': u.last_name
    }


@users.route('/me', methods=['GET'])
@auth.login_required
def get_me():
    """
    @api {get} /users/me Get my account
    @apiVersion 0.1.0
    @apiName GetMe
    @apiGroup User

    @apiSuccess {Number} id             The unique ID of the user.
    @apiSuccess {String} email          The email address of the user.
    @apiSuccess {String} first_name     The first name of the user.
    @apiSuccess {String} last_name      The last name of the user.
    """
    user = User.query.filter_by(id=g.user.id).first()
    return jsonify(parse_user(user))
