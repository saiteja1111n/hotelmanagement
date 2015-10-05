#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
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
    number = ndb.IntegerProperty(indexed =False)
    status = ndb.StringProperty(indexed = False)

class Person(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    mailId = ndb.StringProperty(indexed=True)
    phno = ndb.StringProperty(indexed=False)
    address=ndb.StringProperty(indexed = False)
    type = ndb.StringProperty(indexed=False)
    bookedrooms = ndb.StructuredProperty(Room,repeated=True)

class Hotel(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    admin=ndb.StructuredProperty(Person)
    rooms = ndb.StructuredProperty(Room, repeated=True)

class loginhome(webapp2.RequestHandler):
    def get(self):
        user =users.get_current_user()
        template=JINJA_ENVIRONMENT.get_template('loginhome.html')
        logging.error("login error")
        self.response.write(template.render())


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            q1=Person.query(Person.mailId==user.email()).get()
            if q1 is None:
                template=JINJA_ENVIRONMENT.get_template('createprofile.html')
                self.response.write(template.render())
            else:
                if q1.type == 'admin':
                    template=JINJA_ENVIRONMENT.get_template('adminhome.html')
                    self.response.write(template.render())
                else:
                    template=JINJA_ENVIRONMENT.get_template('home.html')
                    self.response.write(template.render())
        else:
            self.redirect(users.create_login_url(self.request.uri))

class userProfile(webapp2.RequestHandler):
    def post(self):
        try:
            user=users.get_current_user()
            if user:
                q=Person.query(Person.mailId != None).count()
                template=None
                if q is not 0:
                    Person(name=self.request.get('name'),mailId=user.email(),phno=self.request.get('phno'),address=self.request.get('address'),type="client").put()
                    template=JINJA_ENVIRONMENT.get_template('home.html')
                else:
                    Person(name=self.request.get('name'),mailId=user.email(),phno=self.request.get('phno'),address=self.request.get('address'),type="admin").put()
                    template=JINJA_ENVIRONMENT.get_template('adminhome.html')
                self.response.write(template.render())
            else:
                self.redirect(users.create_login_url(self.request.uri))
        except Exception,e:
            traceback.print_exc()
            logging.error("error occured.."+str(e))
            self.response.write("Record not saved")

class getname(webapp2.RequestHandler):
    def post(self):
        user=users.get_current_user()
        if user:
            q=Person.query(Person.mailId==user.email()).get()
            obj={u"name":q.name}
            ss=json.dumps(obj)
            self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
            logging.error("Getname")
            self.response.write(ss)
        else:
            self.redirect(users.create_login_url(self.request.uri))

class homepage(webapp2.RequestHandler):
    def post(self):
        user=users.get_current_user()
        if user:
            q=Person.query(Person.mailId==user.email()).get()
            if q is None:
                template=JINJA_ENVIRONMENT.get_template('createprofile.html')
                self.response.write(template.render())
            else:
                if q.type == 'admin':
                    template=JINJA_ENVIRONMENT.get_template('adminhome.html')
                    self.response.write(template.render())
                else:
                    template=JINJA_ENVIRONMENT.get_template('home.html')
                    self.response.write(template.render())
        else:
            self.redirect(users.create_login_url(self.requesuri))


class logout(webapp2.RequestHandler):
    def get(self):
        logout_url = users.create_logout_url('/')
        self.redirect(logout_url)

app = webapp2.WSGIApplication([

    ('/', loginhome),
    ('/createprofile',userProfile),
    ('/getname',getname),
    ('/homepage',homepage),
    ('/login',MainHandler),
    ('/logout',logout)
], debug=True)
