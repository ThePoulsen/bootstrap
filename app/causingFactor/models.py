from app import db
from app.masterData.models import causingFactorType

class causingFactor(db.Model):
    __tablename__ = 'causingFactor'
    __table_args__ = (db.UniqueConstraint('title', 'tenant_uuid'),)

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), nullable=False, unique=True)
    title = db.Column(db.String(), nullable=False)
    desc = db.Column(db.String())
    tenant_uuid = db.Column(db.String(), nullable=False)
    createdBy = db.Column(db.String(), nullable=False)
    created = db.Column(db.DateTime(), nullable=False)
    modifiedBy = db.Column(db.String())
    modified = db.Column(db.DateTime())

    causingFactorType_uuid = db.Column(db.String(), db.ForeignKey('causingFactorType.uuid'), nullable=False)
