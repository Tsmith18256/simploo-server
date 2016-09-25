from flask import g, jsonify

from . import users
from .. import auth
from ..models import User


def parse_user(u, include_email=True):
    user = {
        'id': u.id,
        'first_name': u.first_name,
        'last_name': u.last_name
    }

    if include_email:
        user['email'] = u.email

    return user


@users.route('/<int:id>', methods=['GET'])
def get_user(id):
    """
    @api {get} /users/:id Get user by ID
    @apiVersion 0.1.0
    @apiName GetUserById
    @apiGroup User

    @apiParam {Number} id   The unique ID of the user.

    @apiSuccess {Number} id             The unique ID of the user.
    @apiSuccess {String} first_name     The first name of the user.
    @apiSuccess {String} last_name      The last name of the user.
    """
    user = User.query.filter_by(id=id).first()

    # email property isn't public, must use /me to see it
    return jsonify(parse_user(user, include_email=False))


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
