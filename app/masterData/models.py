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

class country(db.Model):
    __tablename__ = 'country'
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

    subRegion_id = db.Column(db.Integer(), db.ForeignKey(subRegion.id))
    subRegion = db.relationship(subRegion, backref='countries')

class zone(db.Model):
    __tablename__ = 'zone'
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

    country_id = db.Column(db.Integer(), db.ForeignKey(country.id))
    country = db.relationship(country, backref='zones')

class status(db.Model):
    __tablename__ = 'status'
    __table_args__ = (db.UniqueConstraint('title', 'tenant_uuid'),)

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String())
    title = db.Column(db.String(255))
    tenant_uuid = db.Column(db.String())
    createdBy = db.Column(db.String())
    created = db.Column(db.DateTime())
    modifiedBy = db.Column(db.String())
    modified = db.Column(db.DateTime())
