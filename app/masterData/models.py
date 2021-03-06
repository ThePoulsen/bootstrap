from app import db

class region(db.Model):
    __tablename__ = 'region'
    __table_args__ = (db.UniqueConstraint('title', 'tenant_uuid'),
                      db.UniqueConstraint('abbr', 'tenant_uuid'),)

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), nullable=False, unique=True)
    abbr = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    tenant_uuid = db.Column(db.String(), nullable=False)
    createdBy = db.Column(db.String(), nullable=False)
    created = db.Column(db.DateTime(), nullable=False)
    modifiedBy = db.Column(db.String())
    modified = db.Column(db.DateTime())

    subRegions = db.relationship('subRegion', backref='region', lazy='dynamic', passive_deletes='all')

class subRegion(db.Model):
    __tablename__ = 'subRegion'
    __table_args__ = (db.UniqueConstraint('title', 'tenant_uuid'),
                      db.UniqueConstraint('abbr', 'tenant_uuid'),)

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), nullable=False, unique=True)
    abbr = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    tenant_uuid = db.Column(db.String(), nullable=False)
    createdBy = db.Column(db.String(), nullable=False)
    created = db.Column(db.DateTime(), nullable=False)
    modifiedBy = db.Column(db.String())
    modified = db.Column(db.DateTime())
    
    region_uuid = db.Column(db.String(), db.ForeignKey('region.uuid'), nullable=False)

    countries = db.relationship('country', backref='subRegion', lazy='dynamic', passive_deletes='all')

class country(db.Model):
    __tablename__ = 'country'
    __table_args__ = (db.UniqueConstraint('title', 'tenant_uuid'),
                      db.UniqueConstraint('abbr', 'tenant_uuid'),)

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), nullable=False, unique=True)
    abbr = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    tenant_uuid = db.Column(db.String(), nullable=False)
    createdBy = db.Column(db.String(), nullable=False)
    created = db.Column(db.DateTime(), nullable=False)
    modifiedBy = db.Column(db.String())
    modified = db.Column(db.DateTime())

    subRegion_uuid = db.Column(db.String(), db.ForeignKey('subRegion.uuid'), nullable=False)
    zones = db.relationship('zone', backref='country', lazy='dynamic', passive_deletes='all')

class zone(db.Model):
    __tablename__ = 'zone'
    __table_args__ = (db.UniqueConstraint('title', 'tenant_uuid'),
                      db.UniqueConstraint('abbr', 'tenant_uuid'),)

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), nullable=False, unique=True)
    abbr = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    tenant_uuid = db.Column(db.String(), nullable=False)
    createdBy = db.Column(db.String(), nullable=False)
    created = db.Column(db.DateTime(), nullable=False)
    modifiedBy = db.Column(db.String())
    modified = db.Column(db.DateTime())

    country_uuid = db.Column(db.String(), db.ForeignKey('country.uuid'), nullable=False)

class status(db.Model):
    __tablename__ = 'status'
    __table_args__ = (db.UniqueConstraint('title', 'tenant_uuid'),)

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), nullable=False, unique=True)
    title = db.Column(db.String(), nullable=False)
    tenant_uuid = db.Column(db.String(), nullable=False)
    createdBy = db.Column(db.String(), nullable=False)
    created = db.Column(db.DateTime(), nullable=False)
    modifiedBy = db.Column(db.String())
    modified = db.Column(db.DateTime())

class treatmentType(db.Model):
    __tablename__ = 'treatmentType'
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

    treatments = db.relationship('treatment', backref='treatmentType', lazy='dynamic', passive_deletes='all')

class riskResponse(db.Model):
    __tablename__ = 'riskResponse'
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

    treatments = db.relationship('treatment', backref='riskResponse', lazy='dynamic', passive_deletes='all')

class eventType(db.Model):
    __tablename__ = 'eventType'
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

class impact(db.Model):
    __tablename__ = 'impact'
    __table_args__ = (db.UniqueConstraint('title', 'tenant_uuid'),)

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), nullable=False, unique=True)
    value = db.Column(db.Integer(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    cost = db.Column(db.String())
    schedule = db.Column(db.String())
    requirements = db.Column(db.String())
    legal = db.Column(db.String())
    other = db.Column(db.String())
    tenant_uuid = db.Column(db.String(), nullable=False)
    createdBy = db.Column(db.String(), nullable=False)
    created = db.Column(db.DateTime(), nullable=False)
    modifiedBy = db.Column(db.String())
    modified = db.Column(db.DateTime())

    ratings = db.relationship('rating', backref='impact', lazy='dynamic', passive_deletes='all')
    risks = db.relationship('risk', backref='impact', lazy='dynamic', passive_deletes='all')

class probability(db.Model):
    __tablename__ = 'probability'
    __table_args__ = (db.UniqueConstraint('title', 'tenant_uuid'),)

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), nullable=False, unique=True)
    value = db.Column(db.Integer(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    desc = db.Column(db.String())
    tenant_uuid = db.Column(db.String(), nullable=False)
    createdBy = db.Column(db.String(), nullable=False)
    created = db.Column(db.DateTime(), nullable=False)
    modifiedBy = db.Column(db.String())
    modified = db.Column(db.DateTime())

    ratings = db.relationship('rating', backref='probability', lazy='dynamic', passive_deletes='all')
    risks = db.relationship('risk', backref='probability', lazy='dynamic', passive_deletes='all')

class causingFactorType(db.Model):
    __tablename__ = 'causingFactorType'
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

    causingFactors = db.relationship('causingFactor', backref='causingFactorType', lazy='dynamic', passive_deletes='all')

class processArea(db.Model):
    __tablename__ = 'processArea'
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

class riskArea(db.Model):
    __tablename__ = 'riskArea'
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

    risks = db.relationship('risk', backref='riskArea', lazy='dynamic', passive_deletes='all')

class riskType(db.Model):
    __tablename__ = 'riskType'
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

    risks = db.relationship('risk', backref='riskType', lazy='dynamic', passive_deletes='all')

class valueChainArea(db.Model):
    __tablename__ = 'valueChainArea'
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

    valueChains = db.relationship('valueChain', backref='valueChainArea', lazy='dynamic', passive_deletes='all')

class valueChainStepType(db.Model):
    __tablename__ = 'valueChainStepType'
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

class deliveryPoint(db.Model):
    __tablename__ = 'deliveryPoint'
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
