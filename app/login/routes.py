import requests
from flask import g, jsonify, request
from flask_httpauth import HTTPBasicAuth

from . import login
from .. import db
from ..models import User

FACEBOOK_LOGIN_URL = 'https://graph.facebook.com/me?' \
                     'fields=id,email,name,name_format&access_token={}'

auth = HTTPBasicAuth()


def parse_user(u):
    return {
        'id': u.id,
        'email': u.email,
        'first_name': u.first_name,
        'last_name': u.last_name,
        'social_network_id': u.social_network_id
    }


def find_existing_user(email):
    return User.query.filter_by(email=email).first()


def login_facebook(access_token):
    response = requests.get(FACEBOOK_LOGIN_URL.format(access_token)).json()
    email = response.get('email')

    existing_user = find_existing_user(email)
    if existing_user is not None:
        if existing_user.social_network_id is not 1:
            # Not a Facebook account
            raise ValueError({})    # TODO: throw proper error
        else:
            return existing_user

    names = response.get('name').split()
    fname = names[0]
    lname = names[1]

    user = User(
        email=email,
        first_name=fname,
        last_name=lname,
        social_network_id=1
    )
    db.session.add(user)    # save the user in the database

    return user


@auth.verify_password
def verify_token(token, password):
    print("TOKEN: {}".format(token))
    user = User.verify_auth_token(token)

    if user is None:
        return False

    g.user = user
    return True


@login.route('/token', methods=['POST'])
def login():
    if request.get_json().get('access_token') is None:
        return jsonify({
            'error_type': 'missing_param',
            'missing_param': 'access_token',
            'message': 'access_token is a required parameter'
        })
    elif request.get_json().get('social_network') is None:
        return jsonify({
            'error_type': 'missing_param',
            'missing_param': 'social_network',
            'message': 'social_network is a required parameter'
        }), 400
    elif request.get_json().get('social_network').lower() == 'facebook':
        user = login_facebook(request.get_json().get('access_token'))
        token = user.generate_auth_token()
        return jsonify({
            'access_token': token.decode('ascii')
        })
    else:
        return jsonify({
            'error_type': 'invalid_param',
            'invalid_param': 'social_network',
            'message': 'social_network must be "facebook"'
        })
