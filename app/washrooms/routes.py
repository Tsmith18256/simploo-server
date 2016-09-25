from flask import jsonify, request

from . import washrooms
from ..models import Washroom

HAS_WHEELCHAIR_ACCESS = 'has_wheelchair_access'


def apply_wheelchair_filter(query, filters):
    hwc = filters.get(HAS_WHEELCHAIR_ACCESS)

    if hwc is not None:
        if hwc.lower() == 'true':
            return query.filter_by(has_wheelchair_access=True)
        elif hwc.lower() == 'false':
            return query.filter_by(has_wheelchair_access=False)
        else:
            raise ValueError({
                'error_type': 'invalid_param',
                'invalid_param': 'has_wheelchair_access',
                'message': 'has_wheelchair_access must be "true" or "false"'
            })
    else:
        return query


def apply_filters(query, filters):
    query = apply_wheelchair_filter(query, filters)
    return query


def parse_washroom(w):
    return {
        'id': w.id,
        'name': w.name,
        'description': w.description,
        'latitude': w.latitude,
        'longitude': w.longitude,
        'has_wheelchair_access': w.has_wheelchair_access
    }


@washrooms.route('/', methods=['GET'])
def get_washrooms():
    """
    @api {get} /washrooms/ Get washrooms
    @apiVersion 0.1.0
    @apiName GetWashrooms
    @apiGroup Washroom

    @apiParam {Boolean} has_wheelchair_access   Filters results based on
                                                whether or not the washrooms
                                                have wheelchair access.

    @apiSuccess {Number}    id                      The unique ID of the
                                                    washroom.
    @apiSuccess {String}    name                    The name of the washroom.
    @apiSuccess {String}    description             The description of the
                                                    washroom.
    @apiSuccess {Number}    latitude                The latitude of the
                                                    washroom's location.
    @apiSuccess {Number}    longitude               The longitude of the
                                                    washroom's location.
    @apiSuccess {Boolean}   has_wheelchair_access   Whether or not this
                                                    washroom is
                                                    wheelchair-accessible.
    """
    results = []
    query = Washroom.query

    try:
        query = apply_filters(query, request.args)
    except ValueError as err:
        return jsonify(err.args[0]), 400

    for w in query.all():
        results.append(parse_washroom(w))

    return jsonify(results)


@washrooms.route('/<int:id>', methods=['GET'])
def get_washroom(id):
    """
    @api {get} /washrooms/:id Get washroom by ID
    @apiVersion 0.1.0
    @apiName GetWashroomById
    @apiGroup Washroom

    @apiParam {Number} id   The unique ID of the washroom.

    @apiSuccess {Number}    id                      The unique ID of the
                                                    washroom.
    @apiSuccess {String}    name                    The name of the washroom.
    @apiSuccess {String}    description             The description of the
                                                    washroom.
    @apiSuccess {Number}    latitude                The latitude of the
                                                    washroom's location.
    @apiSuccess {Number}    longitude               The longitude of the
                                                    washroom's location.
    @apiSuccess {Boolean}   has_wheelchair_access   Whether or not this
                                                    washroom is
                                                    wheelchair-accessible.
    """
    w = Washroom.query.filter_by(id=id).first()

    if w is not None:
        return jsonify(parse_washroom(w))
    else:
        return jsonify({
            'error_type': 'invalid_param',
            'invalid_param': 'id',
            'message': 'No washrooms were found with the given ID'
        })
