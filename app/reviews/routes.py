from flask import g, jsonify, request

from . import reviews
from .. import auth, db
from ..models import Feature, Review


def parse_review(r):
    features = []

    for f in r.features:
        features.append({
            'id': f.id,
            'name': f.name,
            'icon': f.icon
        })

    return {
        'id': r.id,
        'user_id': r.user_id,
        'washroom_id': r.washroom_id,
        'description': r.description,
        'cleanliness': r.cleanliness,
        'privacy': r.privacy,
        'safety': r.safety,
        'accessibility': r.accessibility,
        'features': features,
        'rating': r.rating
    }


@reviews.route('/', methods=['GET'])
def get_reviews():
    """
    @api {get} /reviews Get reviews
    @apiVersion 0.1.0
    @apiName GetReviews
    @apiGroup Review

    @apiParam {Number} [washroom_id]    The ID of the washroom to retrieve
                                        reviews for.
    @apiParam {Number} [user_id]        The ID of the user to retrieve reviews
                                        for.

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
    query = Review.query

    w_id = request.args.get('washroom_id')
    u_id = request.args.get('user_id')

    if w_id is not None:
        query = query.filter_by(washroom_id=w_id)

    if u_id is not None:
        query = query.filter_by(user_id=u_id)

    reviews = []
    for r in query.all():
        reviews.append(parse_review(r))

    return jsonify(reviews)


@reviews.route('/', methods=['POST'])
@auth.login_required
def create_review():
    """
    @api {post} /reviews/ Create review
    @apiVersion 0.1.0
    @apiName CreateReview
    @apiGroup Review

    @apiParam {Number}      washroom_id     The ID of the washroom the review
                                            is for.
    @apiParam {String}      [description]   The body text of the review.
    @apiParam {Number{0-5}} cleanliness     The user's cleanliness rating for
                                            the washroom.
    @apiParam {Number{0-5}} privacy         The user's privacy rating for the
                                            washroom.
    @apiParam {Number{0-5}} safety          The user's safety rating for the
                                            washroom.
    @apiParam {Number{0-5}} accessibility   The user's accessibility rating for
                                            the washroom.
    @apiParam {Number[]}    [features]      An array of feature IDs for the
                                            features this washroom has, as
                                            selected by the user.
    """
    existing_review = Review.query.filter_by(
        user_id=g.user.id,
        washroom_id=request.get_json().get('washroom_id')
    ).first()

    if existing_review is not None:
        return jsonify({
            'error_type': 'invalid_param',
            'invalid_param': 'washroom_id',
            'message': 'You cannot have two reviews for the same washroom'
        }), 400

    features = []
    for f in request.get_json().get('features'):
        feature = Feature.query.filter_by(id=f).first()

        if feature is not None:
            features.append(feature)

    review = Review(
        user_id=g.user.id,
        washroom_id=request.get_json().get('washroom_id'),
        description=request.get_json().get('description'),
        cleanliness=request.get_json().get('cleanliness'),
        privacy=request.get_json().get('privacy'),
        safety=request.get_json().get('safety'),
        accessibility=request.get_json().get('accessibility'),
        features=features
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


@reviews.route('/<int:id>', methods=['PUT'])
@auth.login_required
def update_review_by_id(id):
    """
    @api {put} /reviews/:id Update review by ID
    @apiVersion 0.1.0
    @apiName UpdateReviewById
    @apiGroup Review

    @apiParam {Number}      id              The unique ID of the review to
                                            update.
    @apiParam {String}      [description]   The text body of the user's review.
    @apiParam {Number}      [cleanliness]   The user's cleanliness rating for
                                            the washroom.
    @apiParam {Number}      [privacy]       The user's privacy rating for the
                                            washroom.
    @apiParam {Number}      [safety]        The user's safety rating for the
                                            washroom.
    @apiParam {Number}      [accessibility] The user's accessibility rating for
                                            the washroom.
    @apiParam {Number[]}    [features]      The features supported by the
                                            washroom, as selected by the user.
    """
    review = Review.query.filter_by(id=id).first()

    if review is None:
        return jsonify({
            'error_type': 'invalid_param',
            'invalid_param': 'id',
            'message': 'No reviews were found with the given ID'
        }), 400

    if review.user_id == g.user.id:
        if request.get_json().get('description') is not None:
            review.description = request.get_json().get('description')
        if request.get_json().get('cleanliness') is not None:
            review.cleanliness = request.get_json().get('cleanliness')
        if request.get_json().get('privacy') is not None:
            review.privacy = request.get_json().get('privacy')
        if request.get_json().get('safety') is not None:
            review.safety = request.get_json().get('safety')
        if request.get_json().get('accessibility') is not None:
            review.accessibility = request.get_json().get('accessibility')
        if request.get_json().get('features') is not None:
            features = []
            for f in request.get_json().get('features'):
                feature = Feature.query.filter_by(id=f).first()

                if feature is not None:
                    features.append(feature)

            review.features = features

        db.session.add(review)
        return jsonify(parse_review(review))
    else:
        return jsonify({
            'error_type': 'invalid_param',
            'invalid_param': 'id',
            'message': 'You cannot delete somebody else\'s review'
        }), 400


@reviews.route('/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_review_by_id(id):
    """
    @api {delete} /reviews/:id Delete review by ID
    @apiVersion 0.1.0
    @apiName DeleteReviewByID
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

    if r is None:
        return jsonify({
            'error_type': 'invalid_param',
            'invalid_param': 'id',
            'message': 'No reviews were found with the given ID'
        }), 400

    if r.user_id == g.user.id:
        db.session.delete(r)
        return jsonify(parse_review(r))
    else:
        return jsonify({
            'error_type': 'invalid_param',
            'invalid_param': 'id',
            'message': 'You cannot delete somebody else\'s review'
        }), 400
