from app import db

class region(db.Model):
    __tablename__ = 'region'
    __table_args__ = (db.UniqueConstraint('title', 'tenant_uuid'),
                      db.UniqueConstraint('abbr', 'tenant_uuid'),)

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String())
    abbr = db.Column(db.String(10))
    title = db.Column(db.String(255))
    tenant_uuid = db.Column(db.String())
    createdBy = db.Column(db.String())
    created = db.Column(db.DateTime())
    modifiedBy = db.Column(db.String())
    modified = db.Column(db.DateTime())

class subRegion(db.Model):
    __tablename__ = 'subRegion'
    __table_args__ = (db.UniqueConstraint('title', 'tenant_uuid'),
                      db.UniqueConstraint('abbr', 'tenant_uuid'),)

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String())
    abbr = db.Column(db.String(10))
    title = db.Column(db.String(255))
    tenant_uuid = db.Column(db.String())
    createdBy = db.Column(db.String())
    created = db.Column(db.DateTime())
    modifiedBy = db.Column(db.String())
    modified = db.Column(db.DateTime())
    
    region_id = db.Column(db.Integer(), db.ForeignKey(region.id))
    region = db.relationship(region, backref='subRegions')
