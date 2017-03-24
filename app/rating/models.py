from app import db
from app.masterData.models import impact, probability

class rating(db.Model):
    __tablename__ = 'rating'
    __table_args__ = (db.UniqueConstraint('impact_uuid', 'probability_uuid', 'tenant_uuid'),)

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), nullable=False, unique=True)
    value = db.Column(db.Integer(), nullable=False)
    desc = db.Column(db.String())

    tenant_uuid = db.Column(db.String(), nullable=False)
    createdBy = db.Column(db.String(), nullable=False)
    created = db.Column(db.DateTime(), nullable=False)
    modifiedBy = db.Column(db.String())
    modified = db.Column(db.DateTime())

    impact_uuid = db.Column(db.String(), db.ForeignKey('impact.uuid'), nullable=False)
    probability_uuid = db.Column(db.String(), db.ForeignKey('probability.uuid'), nullable=False)
