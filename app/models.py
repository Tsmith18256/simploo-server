from . import db

review_features = db.Table(
    'user_features',
    db.Base.metadata,
    db.Column('review', db.BigInteger, db.ForeignKey('reviews.id')),
    db.Column('feature_id', db.BigInteger, db.ForeignKey('features.id'))
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    first_name = db.column(db.String)
    last_name = db.column(db.String)

    def __repr__(self):
        return '<User %r>' % self.name


class Washroom(db.Model):
    __tablename__ = 'washrooms'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    has_wheelchair_access = db.Column(db.Boolean)

    def __repr__(self):
        return '<Washroom %r>' % self.name


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    washroom_id = db.Column(db.BigInteger, db.ForeignKey('washrooms.id'))
    # rating = db.Column(db.Float)
    description = db.Column(db.String)
    cleanliness = db.Column(db.Integer)
    privacy = db.Column(db.Integer)
    safety = db.Column(db.Integer)
    accessibility = db.Column(db.Integer)
    features = db.relationship('Feature', secondary=review_features)

    def __repr__(self):
        return '<Review %r>' % self.name


class Feature(db.Model):
    __tablename__ = 'features'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String)
    icon = db.Column(db.String)

    def __repr__(self):
        return '<Feature %r>' % self.name
