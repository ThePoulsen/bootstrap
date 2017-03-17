from flask import session
from app.masterData.models import subRegion

def getSubRegions():
    return subRegion.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getSubRegion(uuid):
    pass

def postSubRegion(data):
    pass

def putSubRegion(data, uuid):
    pass

def deleteSubRegion(uuid):
    pass

def subRegionSelectData():
    subRegions = subRegion.query.filter_by(tenant_uuid=session['tenant_uuid']).all()
    dataList = [] #[(0,'')]
    for sr in subRegions:
        dataList.append((sr.uuid, sr.title))
    return dataList

def subRegionListData():
    subRegions = getSubRegions()
    data = []
    for sr in subRegions:
        temp = [sr.uuid, sr.title, sr.abbr, sr.region.abbr]
        data.append(temp)
    return data
