from sqlalchemy.ext.hybrid import hybrid_property

from . import db

review_features = db.Table(
    'user_features',
    db.Column('review', db.BigInteger, db.ForeignKey('reviews.id')),
    db.Column('feature_id', db.BigInteger, db.ForeignKey('features.id'))
)


class SocialNetwork(db.Model):
    __tablename__ = 'social_networks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(31))

    def __repr__(self):
        return '<SocialNetwork %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    social_network_id = db.Column(
        db.Integer,
        db.ForeignKey('social_networks.id')
    )

    def __repr__(self):
        return '<User %r>' % self.name


class Washroom(db.Model):
    __tablename__ = 'washrooms'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
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
    description = db.Column(db.String(255))
    cleanliness = db.Column(db.Integer)
    privacy = db.Column(db.Integer)
    safety = db.Column(db.Integer)
    accessibility = db.Column(db.Integer)
    features = db.relationship('Feature', secondary=review_features)

    @hybrid_property
    def rating(self):
        cleanliness = self.cleanliness
        privacy = self.privacy
        safety = self.safety
        accessibility = self.accessibility

        return (cleanliness + privacy + safety + accessibility) / 4.0

    def __repr__(self):
        return '<Review %r>' % self.name


class Feature(db.Model):
    __tablename__ = 'features'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255))
    icon = db.Column(db.String(255))

    def __repr__(self):
        return '<Feature %r>' % self.name
