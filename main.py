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
    number = ndb.IntegerProperty(indexed =True)
    status = ndb.StringProperty(indexed = True)
    name = ndb.StringProperty(indexed=True)

class Person(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    mailId = ndb.StringProperty(indexed=True)
    phno = ndb.StringProperty(indexed=True)
    address=ndb.StringProperty(indexed = True)
    type = ndb.StringProperty(indexed=True)

class loginhome(webapp2.RequestHandler):
    def get(self):
        user =users.get_current_user()
        template=JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            q1=Person.query(Person.mailId==user.email()).get()
            if q1 is None:
                template=JINJA_ENVIRONMENT.get_template('signup.html')
                self.response.write(template.render())
            else:
                if q1.type == 'admin':
                    template=JINJA_ENVIRONMENT.get_template('adminpage.html')
                    self.response.write(template.render())
                else:
                    template=JINJA_ENVIRONMENT.get_template('users.html')
                    self.response.write(template.render())
        else:
            self.redirect(users.create_login_url(self.request.uri))

class userProfile(webapp2.RequestHandler):
    def post(self):
        try:
            user=users.get_current_user()
            if user:
                q1=Person.query(Person.mailId != None).count()
                q2=Person.query(Person.mailId == user.email()).get()
                template=None
                if q2 is None:
                    if q1 is not 0:
                        Person(name=self.request.get('name'),mailId=user.email(),phno=self.request.get('phno'),address=self.request.get('address'),type="client").put()
                        template=JINJA_ENVIRONMENT.get_template('users.html')
                    else:
                       Person(name=self.request.get('name'),mailId=user.email(),phno=self.request.get('phno'),address=self.request.get('address'),type="admin").put()
                       template=JINJA_ENVIRONMENT.get_template('adminpage.html')
                       for i in range(1,6):
                           Room(number=i,status="available").put()
                    self.response.write(template.render())
                else:
                    if q2.type=="admin":
                        template=JINJA_ENVIRONMENT.get_template('adminpage.html')
                    else:
                        template=JINJA_ENVIRONMENT.get_template('users.html')
                    self.response.write(template.render())
            else:
                self.redirect(users.create_login_url(self.request.uri))
        except Exception,e:
            traceback.print_exc()
            self.response.write("Record not saved")

class getname(webapp2.RequestHandler):
    def post(self):
        user=users.get_current_user()
        if user:
            q=Person.query(Person.mailId == user.email()).get()
            obj = {u"name":q.name}
            ss=json.dumps(obj)
            self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
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
                    template=JINJA_ENVIRONMENT.get_template('adminpage.html')
                    self.response.write(template.render())
                else:
                    template=JINJA_ENVIRONMENT.get_template('users.html')
                    self.response.write(template.render())
        else:
            self.redirect(users.create_login_url(self.requesuri))


class logout(webapp2.RequestHandler):
    def get(self):
        logout_url = users.create_logout_url('/')
        self.redirect(logout_url)

class addroom(webapp2.RequestHandler):
    def post(self):
        user=users.get_current_user()
        if user:
            vals = json.loads(cgi.escape(self.request.body))
            n=int(vals['numberofrooms'])
            q1=Room.query(Room.number!=None).count()
            for i in range(0,n):
                Room(number=i+q1+1,status="available").put()
            obj = {u"meassage":"success"}
            ss=json.dumps(obj)
            self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
            self.response.write(ss)
        else:
            self.redirect(users.create_login_url(self.requesuri))

class getpersonroomstatus(webapp2.RequestHandler):
    def post(self):
        user=users.get_current_user()
        if user:
           query1=Person.query(Person.mailId==user.email()).get()
           logging.error(query1)
           if query1.type == "admin":
               q=Room.query(Room.number!=None)
               list1 = []
               list3 = []
               for q1 in q:
                   stat={"number":q1.number,"status":q1.status}
                   if q1.status == "booked":
                       list1.append(stat)
                   else:
                       list3.append(stat)
               list2  ={"bookedrooms":list1,"availablerooms":list3}
               ss=json.dumps(list2)
               self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
               self.response.write(ss)
           else:
               q=Room.query(ndb.OR(Room.status=="available",Room.name==user.email()))
               list1=[]
               list2=[]
               for q1 in q:
                   if q1.name==user.email():
                       stat={"number":q1.number,"status":q1.status}
                       list1.append(stat)
                   else:
                       stat={"number":q1.number,"status":q1.status}
                       list2.append(stat)
               logging.error(q)
               list3={"bookedrooms":list1,"availablerooms":list2}
               ss=json.dumps(list3)
               self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
               self.response.write(ss)
        else:
            self.redirect(users.create_login_url(self.requesuri))

class removerooms(webapp2.RequestHandler):
    def post(self):
        user=users.get_current_user()
        if user:
           vals = json.loads(cgi.escape(self.request.body))
           n=vals['rooms']
           n1=n.split(",")
           list1=[]
           for n2 in n1:
               q1=Room.query(Room.number==int(n2)).get()
               if q1 is not None:
                   q1.key.delete()
                   logging.error("deleted")
               else:
                   list1.append(n2)
           obj = {u"message":"success",u"unsuccessfull":list1}
           ss=json.dumps(obj)
           self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
           self.response.write(ss)
        else:
            self.redirect(users.create_login_url(self.requesuri))


class cancelbookedroom(webapp2.RequestHandler):
    def post(self):
        user=users.get_current_user()
        if user:
           vals = json.loads(cgi.escape(self.request.body))
           n=vals['rooms']
           n1=n.split(",")
           for n2 in n1:
               q1=Room.query(Room.number==int(n2)).get()
               q1.status="available"
               q1.name=""
               q1.put()
           obj = {u"message":"success"}
           ss=json.dumps(obj)
           self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
           self.response.write(ss)
        else:
            self.redirect(users.create_login_url(self.requesuri))

class bookrooms(webapp2.RequestHandler):
    def post(self):
        user=users.get_current_user()
        if user:
           vals = json.loads(cgi.escape(self.request.body))
           n=vals['rooms']
           n1=n.split(",")
           list1=[]
           for n2 in n1:
               q1=Room.query(Room.number==int(n2)).get()
               if q1 is not None:
                   list1.append(n2)
                   q1.name=user.email()
                   q1.status="booked"
                   q1.put()
           obj = {u"message":"success",u"unsuccessful":list1}
           ss=json.dumps(obj)
           self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
           self.response.write(ss)
        else:
            self.redirect(users.create_login_url(self.requesuri))


class testtemplate(webapp2.RequestHandler):
    def get(self):
        template=JINJA_ENVIRONMENT.get_template('users.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([

    ('/', loginhome),
    ('/createprofile',userProfile),
    ('/getname',getname),
    ('/homepage',homepage),
    ('/login',MainHandler),
    ('/logout',logout),
    ('/addroom',addroom),
    ('/getroomstatus',getpersonroomstatus),
    ('/bookroom',bookrooms),
    ('/test',testtemplate),
    ('/cancelrooms',cancelbookedroom),
    ('/removeroom',removerooms)
], debug=True)
