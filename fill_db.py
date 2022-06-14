from app import db, City

db.drop_all()
db.create_all()

gothenburg = City(name='Göteborg', longitude=57.708870, latitude=11.974560)
db.session.add(gothenburg)
db.session.commit()