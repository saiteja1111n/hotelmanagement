import os
import cgi
import traceback
import json
import jinja2
import webapp2
import logging
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app
from pprint import pprint
import datetime
from datetime import datetime
from random import shuffle

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Room(ndb.Model):
    number = ndb.IntegerProperty(indexed =True)
    status = ndb.StringProperty(indexed = True)
    bookedperson = ndb.StructuredProperty(indexed=True)
    numberofpeople = ndb.IntegerProperty(indexed=True)
    details = ndb.StringProperty(indexed=False)

class Person(ndb.Model):
    name = ndb.StringProperty(indexed= False)
    mailId = ndb.StringProperty(indexed=True)
    phno = ndb.StringProperty(indexed= False)
    address=ndb.StringProperty(indexed = False)
    type = ndb.StringProperty(indexed=True)

