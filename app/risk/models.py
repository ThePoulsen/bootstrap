## -*- coding: utf-8 -*-
from app import db

class risk(db.Model):
    __tablename__ = 'risk'
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

    owner = db.Column(db.String(), db.ForeignKey('user.uuid'), nullable=False)

    riskType_uuid = db.Column(db.String(), db.ForeignKey('riskType.uuid'), nullable=False)
    riskArea_uuid = db.Column(db.String(), db.ForeignKey('riskArea.uuid'), nullable=False)
    probability_uuid = db.Column(db.String(), db.ForeignKey('probability.uuid'), nullable=False)
    impact_uuid = db.Column(db.String(), db.ForeignKey('impact.uuid'), nullable=False)
