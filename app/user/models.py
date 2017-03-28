from app import db

user_groups = db.Table('userGroups',
            db.Column('user_uuid', db.String(), db.ForeignKey('user.uuid')),
            db.Column('group_uuid', db.String(), db.ForeignKey('group.uuid')),
            db.PrimaryKeyConstraint('group_uuid', 'user_uuid'))

class user(db.Model):
    __tablename__ = 'user'
    __table_args__ = (db.UniqueConstraint('initials', 'tenant_uuid'),
                      db.UniqueConstraint('email', 'tenant_uuid'),)

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), nullable=False, unique=True)
    initials = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean())
    locked = db.Column(db.Boolean())
    contact = db.Column(db.Boolean())
    confirmed = db.Column(db.Boolean())

    tenant_uuid = db.Column(db.String(), nullable=False)
    createdBy = db.Column(db.String(), nullable=False)
    created = db.Column(db.DateTime(), nullable=False)
    modifiedBy = db.Column(db.String())
    modified = db.Column(db.DateTime())

    groups = db.relationship('group', secondary=user_groups, backref=db.backref('userGroups', lazy='dynamic'))
    risks = db.relationship('risk', backref='riskOwner', lazy='dynamic', passive_deletes='all')

class group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), nullable=False, unique=True)
    title = db.Column(db.String(), nullable=False)
    desc = db.Column(db.String())

    tenant_uuid = db.Column(db.String(), nullable=False)
    createdBy = db.Column(db.String(), nullable=False)
    created = db.Column(db.DateTime(), nullable=False)
    modifiedBy = db.Column(db.String())
    modified = db.Column(db.DateTime())

    users = db.relationship('user', secondary=user_groups,
                            backref=db.backref('groupUsers', lazy='dynamic'))
