import json
import webapp2
import os
import jinja2
import random
import time
import urllib


from models import User, Event, UserEvent
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import urlfetch



jinja_current_directory = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class HomePageHandler(webapp2.RequestHandler):
    def get(self):
        loggedin_user = users.get_current_user()

        if loggedin_user:
            print('logged in with: ' + loggedin_user.user_id())
            current_user = User.query(User.id == loggedin_user.user_id()).get()
            if current_user == None:
                print('user does not exist')
                template = jinja_current_directory.get_template('templates/signup.html')
                self.response.write(template.render())
            else:
                print('user does exist')
                url = 'https://app.ticketmaster.com/discovery/v2/events.json?classificationName=music&dmaId=324&apikey=zjreZ4GpbxN2WwZfOOKPooZF2FkTrZKe'
                fetch_result = urlfetch.fetch(url)
                fetch_content = json.loads(fetch_result.content)
                api_event_list = fetch_content['_embedded']['events']

                for api_event in api_event_list:
                    event = Event(name=api_event['name'], venue=api_event['_embedded']['venues'][0]['name'],
                    date= api_event['dates']['start']['localDate'], description=api_event['url'],
                    image=api_event['_embedded']['attractions'][0]['images'][0]['url'])
                    event_exists = Event.query(Event.description == api_event['url']).get()
                    if event_exists:
                        pass
                    else:
                        event.put()





                template = jinja_current_directory.get_template('templates/homepage.html')
                self.response.write(template.render({'logout_link': users.create_logout_url('/')}))
        else:
            print('not logged in')
            login_prompt_template = jinja_current_directory.get_template('templates/login.html')
            self.response.write(login_prompt_template.render({'login_link': users.create_login_url('/')}))


class MakeUser(webapp2.RequestHandler):
    def post(self):
        user = User(first_name = self.request.get('firstname'),
        id = users.get_current_user().user_id(),
        last_name = self.request.get('lastname'),
        email = users.get_current_user().email(),
        city = self.request.get('city'))
        user.put()
        time.sleep(.25)
        self.redirect('/')


class EventListHandler(webapp2.RequestHandler):
    def get(self):
        self.response.content_type = 'text/json'
        events = Event.query().fetch()
        events_list = []
        for event in events:
            events_list.append({
                'name' : event.name,
                'venue' : event.venue,
                'description' : event.description,
                'image': event.image,
                #'artist': event.artist,
                'date': event.date,
                'key': str(event.key.id()),

            })
        self.response.write(json.dumps(events_list))


class GroupPageHandler(webapp2.RequestHandler):
    def post(self):
        event_key = self.request.get('event_chosen')
        UserEvents = UserEvent.query().filter(UserEvent.event_key == event_key)
        UserList = []
        for i in range(len(UserEvents)):
            user_key = UserEvents[i].user_key
            user = user_key.get()
            UserList.append(user)


class EmailListHandler(webapp2.RequestHandler):
    def get(self):
        event_key_id = self.request.get('event_key_id')
        event_key = ndb.Key(Event, int(event_key_id) )
        event = Event.query(Event.key == event_key).get()
        loggedin_user = users.get_current_user()
        user = User.query(loggedin_user.user_id() == User.id).get()
        newUserEvent = UserEvent(user_key= user.key, event_key= event.key)
        currentUserEvent = UserEvent.query(ndb.AND((UserEvent.user_key==user.key),(UserEvent.event_key==event.key))).get()
        if currentUserEvent == None:
            newUserEvent.put()
            time.sleep(.25)
        UserEvents = UserEvent.query(UserEvent.event_key == event_key).fetch()
        Users = []
        for userevent in UserEvents:
            user = userevent.user_key.get()
            Users.append(user)
        Users.sort()
        template = jinja_current_directory.get_template('templates/emaillist.html')
        self.response.write(template.render(Users=Users, event = event))







app = webapp2.WSGIApplication([
    ('/eventlist', EventListHandler),
    ('/emaillist', EmailListHandler),
    ('/', HomePageHandler),
    ('/makeuser', MakeUser)
], debug=True)
