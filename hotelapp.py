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

class Person(ndb.Model):
    # roomsbooked = ndb.StringProperty(repeated=True)
    mailId = ndb.StringProperty(indexed=True)
    phno = ndb.StringProperty(indexed= False)
    Name = ndb.StringProperty(indexed = False)
    # bookingstatus = ndb.BooleanProperty(indexed = False,default=False)

class Room(ndb.Model):
    number = ndb.StringProperty(indexed =True)
    status = ndb.StringProperty(indexed = True)
    type = ndb.IntegerProperty(indexed=True)
    acstatus = ndb.BooleanProperty(indexed=True)
    cost = ndb.IntegerProperty(indexed=True)
    frm_date = ndb.DateTimeProperty()
    to_date = ndb.DateTimeProperty()
    customer = ndb.StructuredProperty(Person)

class Admin(ndb.Model):
    Name = ndb.StringProperty(indexed = True)
    customerfeedback  = ndb.StringProperty(repeated = True)

class Userfeedbacks(ndb.Model):
    user = ndb.StructuredProperty(Person)
    rating = ndb.StringProperty(indexed = False)
    message = ndb.StringProperty(indexed = False)
    status = ndb.StringProperty(indexed = True)
    date = ndb.DateTimeProperty(auto_now_add=True)




class indexPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("fdfsd")
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

class confirmrequest(webapp2.RequestHandler):
    def post(self):
        vals = json.loads(cgi.escape(self.request.body))
        room_numbers = vals['booked_rooms'].split(',')
        room_list=[]
        for s in room_numbers:
            s = s.strip(' \t\n\r')
            q1 = Room.query(Room.number==s).get()
            p=Person(Name=vals['person_name'],mailId=vals['person_email'],phno=vals['person_mobileno'])
            if q1:
                q1.customer=p
                q1.frm_date = datetime.strptime(vals['start_date'], "%Y-%m-%d")
                q1.to_date =datetime.strptime(vals['end_date'], "%Y-%m-%d")
                q1.status="awaiting"
                q1.put()
                message = {"message":"success"}
            else:
                message = {"message":"failure","error":"could not find the room that is booked in database"}
        data = json.dumps(message)
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.write(data)

class contactpage(webapp2.RequestHandler):
    def get(self):
        template=JINJA_ENVIRONMENT.get_template('contact.html')
        self.response.write(template.render())


class savefeedback(webapp2.RequestHandler):
    def post(self):
        vals = json.loads(cgi.escape(self.request.body))
        f = Userfeedbacks(user=Person(Name=vals['name'], mailId=vals['email'], phno=vals['phone']), status="unread", message = vals['msg'], rating=vals['rating'])
        f.put()
        message = {"message":"success"}
        data = json.dumps(message)
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.write(data)


class adminpage(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        if user:
            template=JINJA_ENVIRONMENT.get_template('index.html')
            f1 =Userfeedbacks.query().fetch()
            fl1=[]
            fl2=[]
            for f in f1:
                if f.status == "unread":
                    fl1.append(f)
                else:
                    fl2.append(f)
            p1 = Room.query().fetch()
            bl1=[]
            bl2=[]
            for p in p1:
                if p.status == "awaiting":
                    bl1.append(p)
                elif p.status == "confirmed":
                    bl2.append(p)
            template_values = {
                'user': user,
                'unreadfeeds': fl1,
                'readfeeds':fl2,
                'confirmed_bookings': bl2,
                'unconfirmed_bookings':bl1,
            }
            self.response.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))

class confirm_room(webapp2.RequestHandler):
    def post(self):
        vals = json.loads(cgi.escape(self.request.body))
        rm = Room.query(Room.number==str(vals['roomno'])).get()
        message={}
        if rm:
            rm.status="confirmed"
            rm.put()
            message={"message":"success"}
        else:
            message={"message":"failed to confirm room"}
        data = json.dumps(message)
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.write(data)


class cancel_room(webapp2.RequestHandler):
    def post(self):
        vals = json.loads(cgi.escape(self.request.body))
        rm = Room.query(Room.number==str(vals['roomno'])).get()
        message={}
        if rm:
            rm.status="available"
            rm.put()
            message={"message":"success"}
        else:
            message={"message":"failed to confirm room"}
        data = json.dumps(message)
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.write(data)

class add_room(webapp2.RequestHandler):
    def post(self):
        vals=json.load(cgi.escape(self.request.body))
        s = Room(number=vals['room_number'],status="available",type=vals['room_type'],acstatus=vals['ac_type'],cost=vals['room_cost'])
        s.put();
        message={"message":"room added. Please refresh to see the update"}
        data = json.dumps(message)
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.write(data)

app = webapp2.WSGIApplication([
    ('/', indexPage),
    ('/availablerooms', getavailableRooms),
    ('/conformrequest', confirmrequest),
    ('/contact',contactpage),
    ('/feedback',savefeedback),
    ('/admin', adminpage),
    ('/confirm_rm',confirm_room),
    ('/cancel_rm',cancel_room),
    ('/addroom',add_room),
], debug=True)
