from app import db, City

db.drop_all()
db.create_all()

gothenburg = City(name='Göteborg', longitude=11.974560, latitude=57.708870)
db.session.add(gothenburg)
db.session.commit()