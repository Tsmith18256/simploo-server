from flask import jsonify

from . import washrooms
from flask import request

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


def apply_filters(query, filters):
    query = apply_wheelchair_filter(query, filters)
    return query


@washrooms.route('/', methods=['GET'])
def get_washrooms():
    """
    @api {get} /washrooms/ Get washrooms
    @apiName GetWashrooms
    @apiGroup Washroom

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
        results.append({
            'id': w.id,
            'name': w.name,
            'description': w.description,
            'latitude': w.latitude,
            'longitude': w.longitude,
            'has_wheelchair_access': w.has_wheelchair_access
        })

    return jsonify(results)
