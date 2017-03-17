from app import db

class region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    abbr = db.Column(db.String(10), unique=True)
    title = db.Column(db.String(255), unique=True)
    tenant_uuid = db.Column(db.String())

class subRegion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    abbr = db.Column(db.String(10), unique=True)
    title = db.Column(db.String(255), unique=True)
    tenant_uuid = db.Column(db.String())
    
    region_id = db.Column(db.Integer(), db.ForeignKey(region.id))
    region = db.relationship(region, backref='subRegions')