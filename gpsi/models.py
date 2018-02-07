import datetime

from geoalchemy2 import Geography

from gpsi import db


class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    points = db.relationship('WayPoint', backref='route', lazy=True)

    def __repr__(self):
        return '<Route: %r>' % self.id


class WayPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'),
        nullable=False)
    coordinate = db.Column(Geography(geometry_type='POINT', srid=4326))

    def __repr__(self):
        return '<WayPoint: %s>' % self.coordinate
