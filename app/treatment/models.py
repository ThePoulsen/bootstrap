## -*- coding: utf-8 -*-

from app import db
from app.masterData.models import treatmentType, riskResponse

class treatment(db.Model):
    __tablename__ = 'treatment'
    __table_args__ = (db.UniqueConstraint('title', 'tenant_uuid'),)

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), nullable=False, unique=True)
    title = db.Column(db.String(), nullable=False)
    desc = db.Column(db.String(), nullable=False)

    tenant_uuid = db.Column(db.String(), nullable=False)
    createdBy = db.Column(db.String(), nullable=False)
    created = db.Column(db.DateTime(), nullable=False)
    modifiedBy = db.Column(db.String())
    modified = db.Column(db.DateTime())

    treatmentType_id = db.Column(db.Integer, db.ForeignKey('treatmentType.id'))
    treatmentType = db.relationship('treatmentType', backref=db.backref('posts', lazy='dynamic'))

    riskResponse_id = db.Column(db.Integer, db.ForeignKey('riskResponse.id'))
    riskResponse = db.relationship('riskResponse', backref=db.backref('posts', lazy='dynamic'))
