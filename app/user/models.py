from app import db

class user(db.Model):
    __tablename__ = 'user'
    __table_args__ = (db.UniqueConstraint('initials', 'tenant_uuid'),
                      db.UniqueConstraint('email', 'tenant_uuid'),)

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), nullable=False)
    initials = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    roles = db.Column(db.String(), nullable=False)
    groups = db.Column(db.String(), nullable=False)
    token = db.Column(db.String())
    contact = db.Column(db.Boolean())

    tenant_uuid = db.Column(db.String(), nullable=False)
    createdBy = db.Column(db.String(), nullable=False)
    created = db.Column(db.DateTime(), nullable=False)
    modifiedBy = db.Column(db.String())
    modified = db.Column(db.DateTime())

class roles():
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=False)

class groups():
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=False)

    tenant_uuid = db.Column(db.String(), nullable=False)
    createdBy = db.Column(db.String(), nullable=False)
    created = db.Column(db.DateTime(), nullable=False)
    modifiedBy = db.Column(db.String())
    modified = db.Column(db.DateTime())
