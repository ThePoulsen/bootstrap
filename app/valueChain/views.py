## -*- coding: utf-8 -*-

from flask import render_template, Blueprint, flash, request, session, redirect, url_for, jsonify
from app.services.services import errorMessage, successMessage, loginRequired, requiredRole
from app.crud import userCrud, groupCrud

valueChainBP = Blueprint('valueChainBP', __name__)

# valueChainView
@valueChainBP.route('/', methods=['GET','POST'])
@loginRequired
def valueChainView():
    return 'vc'
