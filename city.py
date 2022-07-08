from base import db
from sqlalchemy.orm import relationship

class City(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(50), unique=True, nullable=False)
    longitude = db.Column(db.Float, nullable=True)
    latitude  = db.Column(db.Float, nullable=True)
    weathers  = relationship('Weather')
    # pollens   = relationship('Pollen')
    # uvs       = relationship('UV')

    def __repr__(self):
        return '<City {}: {} {} {}>'.format(self.id, self.name, self.longitude, self.latitude)

    def serialize(self):
        return dict(id=self.id, name=self.name, longitude=self.longitude, latitude=self.latitude)
