def create_point_from_dict(coord_dict):
    """ Returns Text form from a dictionary containing cooridantes.
    """
    lat = coord_dict['lat']
    lon = coord_dict['lon']
    return 'POINT({} {})'.format(lon, lat)
