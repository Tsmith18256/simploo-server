from flask import g, jsonify, request

from . import reviews
from .. import auth, db
from ..models import Review


def parse_review(r):
    return {
        'id': r.id,
        'user_id': r.user_id,
        'washroom_id': r.washroom_id,
        'description': r.description,
        'cleanliness': r.cleanliness,
        'privacy': r.privacy,
        'safety': r.safety,
        'accessibility': r.accessibility,
        'features': r.features,
        'rating': r.rating
    }


@reviews.route('/', methods=['POST'])
@auth.login_required
def create_review():
    review = Review(
        user_id=g.user.id,
        washroom_id=request.get_json().get('washroom_id'),
        description=request.get_json().get('description'),
        cleanliness=request.get_json().get('cleanliness'),
        privacy=request.get_json().get('privacy'),
        safety=request.get_json().get('safety'),
        accessibility=request.get_json().get('accessibility')
    )
    db.session.add(review)

    return jsonify(parse_review(review))


@reviews.route('/<int:id>', methods=['GET'])
def get_review_by_id(id):
    """
    @api {get} /reviews/:id Get review by ID
    @apiVersion 0.1.0
    @apiName GetReviewById
    @apiGroup Review

    @apiParam {Number} id   The unique ID of the review.

    @apiSuccess {Number}    id              The unique ID of the review.
    @apiSuccess {Number}    user_id         The ID of the user that wrote the
                                            review.
    @apiSuccess {Number}    washroom_id     The ID of the washroom being
                                            reviewed.
    @apiSuccess {String}    description     The text body of the user's review.
    @apiSuccess {Number}    rating          The user's overall rating of the
                                            washroom.
    @apiSuccess {Number}    cleanliness     The user's cleanliness rating for
                                            the washroom.
    @apiSuccess {Number}    privacy         The user's privacy rating for the
                                            washroom.
    @apiSuccess {Number}    safety          The user's safety rating for the
                                            washroom.
    @apiSuccess {Number}    accessibility   The user's accessibility rating for
                                            the washroom.
    @apiSuccess {Object[]}  features        The features supported by the
                                            washroom, as selected by the user.
    """
    r = Review.query.filter_by(id=id).first()

    if r is not None:
        return jsonify(parse_review(r))
    else:
        return jsonify({
            'error_type': 'invalid_param',
            'invalid_param': 'id',
            'message': 'No reviews were found with the given ID'
        })
