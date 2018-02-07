from flask import jsonify, request

from gpsi import app, db
from gpsi.models import Route, WayPoint
from gpsi.utils import create_point_from_dict


@app.route('/route/', methods=['POST'])
def routes():
    """ Creates a route, returns a route with a new id.
    """
    route = Route()
    db.session.add(route)
    db.session.commit()
    return_dict = {
        'route_id': route.id
    }
    return jsonify(return_dict)


@app.route('/route/<int:route_id>/way_point/', methods=['POST'])
def way_points(route_id):
    """ Add a way point to a route.
    """

    route = db.session.query(Route).get(route_id)
    if not route:
        return '', 404

    # TODO: Validate the post data is clean/sane
    point = create_point_from_dict(request.form)
    way_point = WayPoint(route_id=route.id, coordinate=point)
    db.session.add(way_point)
    db.session.commit()
    return '', 201


@app.route('/route/<int:route_id>/length/', methods=['GET'])
def length(route_id):
    """ Calculate the lenght of the a route.
    """

    route = db.session.query(Route).get(route_id)
    if not route:
        return '', 404

    # TODO: USE the ORM Directly
    length_query = """
        SELECT ST_Length(ST_MakeLine(ST_AsText(coordinate))::geography)
        FROM way_point
        WHERE route_id={};
    """.format(route.id)
    length = db.engine.execute(length_query).fetchone()[0]

    # Convert into KMs
    if length:
        length = length / 1000
    else:
        length = 0

    length_dict = {
        'km': length
    }
    return jsonify(length_dict)
