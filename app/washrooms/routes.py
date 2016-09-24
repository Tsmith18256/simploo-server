from flask import jsonify

from . import washrooms
from ..models import Washroom


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
    for w in Washroom.query.all():
        results.append({
            'id': w.id,
            'name': w.name,
            'description': w.description,
            'latitude': w.latitude,
            'longitude': w.longitude,
            'has_wheelchair_access': w.has_wheelchair_access
        })

    return jsonify(results)
