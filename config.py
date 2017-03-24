## -*- coding: utf-8 -*-
# project/config.py
import os
import vars
path = os.path.join('.', os.path.dirname(__file__), 'app/static/js/sijax/')

mail                                    = os.environ['mail']
mailPass                                = os.environ['mailPass'].replace("'","")
secretKey                               = os.environ['secretKey']
mailSender                              = os.environ['mailSender']
mailServer                              = os.environ['mailServer']
mailPort                                = os.environ['mailPort']
mailSSL                                 = os.environ['mailSSL']
secretKey                               = os.environ['secretKey']

class BaseConfig(object):
    MAIL_USERNAME                       = mail
    MAIL_PASSWORD                       = mailPass
    MAIL_DEFAULT_SENDER                 = mailSender
    MAIL_SERVER                         = mailServer
    MAIL_PORT                           = int(mailPort)
    MAIL_USE_SSL                        = bool(mailSSL)
    SECRET_KEY                          = secretKey
    SIJAX_STATIC_PATH                   = path
    SIJAX_JSON_URI                      = 'app/static/js/sijax/json2.js'
    JSON_AS_ASCII                       = False
    TEMPLATES_AUTO_RELOAD               = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI             = os.environ['db']
    SQLALCHEMY_TRACK_MODIFICATIONS      = True
    MINIFY_PAGE                         = False

class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI             = 'sqlite:///'
    DEBUG                               = True
    TESTING                             = True

class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI             = os.environ['db']
    SQLALCHEMY_TRACK_MODIFICATIONS      = False
    MINIFY_PAGE                         = True
