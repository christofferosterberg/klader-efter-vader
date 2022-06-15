from app import db, City

db.drop_all()
db.create_all()

stockholm  = City(name='Stockholm', longitude=18.0686, latitude=59.3294)
gothenburg = City(name='Göteborg', longitude=11.9810, latitude=57.6717)
malmo      = City(name='Malmö', longitude=13.0214, latitude=55.5932)

db.session.add(stockholm)
db.session.add(gothenburg)
db.session.add(malmo)
db.session.commit()