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
    number = ndb.StringProperty(indexed =True)
    status = ndb.StringProperty(indexed = True)
    type = ndb.IntegerProperty(indexed=True)
    acstatus = ndb.BooleanProperty(indexed=True)
    cost = ndb.IntegerProperty(indexed=True)

class Person(ndb.Model):
    roomsbooked = ndb.StructuredProperty(Room,repeated=True)
    mailId = ndb.StringProperty(indexed=True)
    phno = ndb.StringProperty(indexed= False)
    Name = ndb.StringProperty(indexed = False)


class indexPage(webapp2.RequestHandler):
    def get(self):
        que1 = Room.query().count()
        if que1 == 0:
            for i in range(1,4):
                for j in range(1,5):
                    Room(number=str(i)+str(j),status="available",type=i,acstatus=True,cost=1000*i).put()
        template=JINJA_ENVIRONMENT.get_template('index1.html')
        self.response.write(template.render())

class getavailableRooms(webapp2.RequestHandler):
    def post(self):
        avaiable_rooms = Room.query(Room.status == "available")
        single_room_list = []
        double_room_list = []
        triple_room_list = []
        for q in avaiable_rooms:
            if q.type == 1:
                s = {'number':q.number,'acstatus':q.acstatus,'cost':q.cost}
                single_room_list.append(s)
            elif q.type == 2:
                s = {'number':q.number,'acstatus':q.acstatus,'cost':q.cost}
                double_room_list.append(s)
            else:
                s = {'number':q.number,'acstatus':q.acstatus,'cost':q.cost}
                triple_room_list.append(s)
        total_rooms = {"single_rooms":single_room_list,"double_rooms":double_room_list,"triple_rooms":triple_room_list}
        total_rooms = json.dumps(total_rooms)
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.write(total_rooms)


app = webapp2.WSGIApplication([
    ('/', indexPage),
    ('/availablerooms', getavailableRooms)
], debug=True)
