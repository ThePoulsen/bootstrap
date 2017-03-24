from app import db

class log(db.Model):
    __tablename__ = 'log'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime(), nullable=False)
    tenant_uuid = db.Column(db.String(), nullable=False)
    user_uuid = db.Column(db.String(), nullable=False)
    table = db.Column(db.String())
    tableRow_uuid = db.Column(db.String())
    event = db.Column(db.String(), nullable=False)
