from app import db

class Imports(db.Model):
    __tablename__ = 'imports'
    import_id = db.Column(db.Integer, autoincrement=True, primary_key=True)


class Citizen(db.Model):
    __tablename__ = 'citizens'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    imports = db.relationship("Imports", backref="citizens")
    import_id = db.Column(db.Integer, db.ForeignKey(
        'imports.import_id', ondelete='CASCADE'))

    citizen_id = db.Column(db.Integer)
    town = db.Column(db.String(256))
    street = db.Column(db.String(256))
    building = db.Column(db.String(256))
    appartement = db.Column(db.Integer)
    name = db.Column(db.String(256))
    birth_date = db.Column(db.String(256))
    gender = db.Column(db.String(256))

    kindred = db.Table('relatives',
        db.Column('citizen_id', db.Integer, db.ForeignKey('citizens.citizen_id')),
        db.Column('relatives_id', db.Integer, db.ForeignKey('citizens.citizen_id'))
    )

    relatives = db.relationship('Citizen',
        secondary = kindred, 
        primaryjoin = (kindred.c.citizen_id == id), 
        secondaryjoin = (kindred.c.relatives_id == id),
        backref = db.backref('kindred', lazy = 'dynamic'),
        lazy = 'dynamic'
    )