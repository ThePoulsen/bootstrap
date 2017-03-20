from app import db
from flask import session
from app.masterData.models import likelihood
import uuid as UUID
from datetime import datetime

def getLikelihoods():
    return likelihood.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getLikelihood(uuid):
    return likelihood.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postLikelihood(data):
    pass

def putLikelihood(data, uuid):
    pass

def deleteLikelihood(uuid):
    pass

def likelihoodSelectData():
    pass

def likelihoodListData():
    pass
