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
    type = ndb.StringProperty(indexed=False)

class Room(ndb.Model):
    hotelname = 

class Hotel(ndb.Model):
	hotelname = ndb.StringProperty(indexed=True)
	roomsavailable = ndb.IntegerProperty(indexed=True)
	bookedrooms = ndb.IntegerProperty(indexed=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('home.html')
        if user:
            self.response.write(template.render())
        else:
            self.redirect(users.create_login_url(self.request.uri))



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/asd',MainHandler)
], debug=True)
