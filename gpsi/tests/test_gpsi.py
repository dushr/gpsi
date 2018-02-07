from flask import json

from hamcrest import assert_that, has_entries, instance_of, equal_to

from gpsi.models import Route, WayPoint
from gpsi.utils import create_point_from_dict
from gpsi.tests import GPSITests


class TestRoute(GPSITests):

    def test_create_route(self):
        resp = self.app.post('/route/')
        route = json.loads(resp.data)

        # Assert the return format
        assert_that(route, has_entries({
            'route_id': instance_of(int)
        }))
        # Now check if it is actually in the db
        route_id = route['route_id']
        route_from_db = self.db.session.query(Route).get(route_id)
        assert_that(route_from_db.id, equal_to(route_id))


class TestWayPoint(GPSITests):

    fixtures = [Route()]

    def setUp(self):
        self.route = self.fixtures[0]

    def test_create_waypoint_route_does_not_exist(self):
        resp = self.app.post(
            '/route/3333/way_point/',
            data={'lat': 1, 'lon': 2}
        )
        assert_that(resp.status_code, equal_to(404))

    def test_create_waypoint(self):
        endpoint = '/route/{}/way_point/'.format(self.route.id)
        resp = self.app.post(
            endpoint,
            data={"lat": -25.4025905, "lon": -49.3124416}
        )
        assert_that(resp.status_code, equal_to(201))


class TestWayPointLength(GPSITests):

    @classmethod
    def load_fixtures(cls):
        cls.route = Route()
        cls.db.session.add(cls.route)
        cls.db.session.flush()
        cls.fixtures = [
            WayPoint(
                route_id=cls.route.id,
                coordinate=create_point_from_dict(
                    {"lat": -25.4025905, "lon": -49.3124416}
                )),
            WayPoint(
                route_id=cls.route.id,
                coordinate=create_point_from_dict(
                    {"lat": 59.3258414, "lon": 17.70188}
                )),
            WayPoint(
                route_id=cls.route.id,
                coordinate=create_point_from_dict(
                    {"lat": 53.200386, "lon": 45.021838}
                )),
        ]
        super(TestWayPointLength, cls).load_fixtures()

    def test_length(self):
        endpoint = '/route/{}/length/'.format(self.route.id)
        resp = self.app.get(endpoint)
        assert_that(resp.status_code, equal_to(200))

        length = json.loads(resp.data)
        # Assert the return format
        assert_that(length, has_entries({
            'km': instance_of(float)
        }))
        # Assert the return lenght is correct
        assert 12975 < length['km'] < 13025
