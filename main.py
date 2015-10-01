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


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Person(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    mailId = ndb.StringProperty(indexed=True)
    phno = ndb.StringProperty(indexed=False)
    adderss=ndb.StringProperty(indexed = False)
    type = ndb.StringProperty(indexed=False)

class Room(ndb.Model):
    number = ndb.IntegerProperty(indexed =False)
    facilities = ndb.StringProperty(indexed = False)
    status = ndb.StringProperty(indexed = False)

class Hotel(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    admin=ndb.StructuredProperty(Person)
    rooms = ndb.StructuredProperty(Room, repeated=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('createprofile.html')
        if user:
            q1=Person.query(Person.mailId==user.email())
            if q1 is None:
                template=JINJA_ENVIRONMENT.get_template('createprofile.html')
                self.response.write(template.render())
            self.response.write(template.render())
        else:
            self.redirect(users.create_login_url(self.request.uri))

class userProfile(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user();
        vale = json.loads(cgi.escape(self.request.body))
        vals=vale['jsonData']
        q=Hotel.query()
        if q is not None:
            if q.admin is not None:
                Person(name=vals['name'],mailId=user.email(),phno=vals['phno'],address=vals['address'],type="client").put()
            else:
                Person(name=vals['name'],mailId=user.email(),phno=vals['phno'],address=vals['address'],type="admin").put()
        else:
            Person(name=vals['name'],mailId=user.email(),phno=vals['phno'],address=vals['address'],type="admin").put()

        obj = {u"testEnd":"succcersss"}
        template = JINJA_ENVIRONMENT.get_template('home.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/createprofile',userProfile)
], debug=True)
