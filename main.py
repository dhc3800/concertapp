import json
import webapp2
import os
import jinja2
import random
import time



from models import User, Event, UserEvent
from google.appengine.api import users
from google.appengine.ext import ndb

event1 = Event(name = 'Pink', venue = 'LAX', description = 'Its a concert', artist = 'Pink', date = 'October 12, 2018', image = 'https:\/\/s1.ticketm.net\/dam\/a\/1dd\/d5e86d93-5e1a-49d9-b530-70fefc0f21dd_711081_ARTIST_PAGE_3_2.jpg')
event2 = Event(name = 'Lebron', venue = 'Staples', description = 'Its a basketball game', artist = 'Lebronto', date = 'Novermber 15, 2019', image = 'https://cdn-s3.si.com/s3fs-public/2018/07/30/lebron-james-possible-second-return-to-cavaliers.jpg')
event3 = Event(name = 'Band', venue = 'Nhhs', description = 'Its a shitty concert', artist = 'Jazz Band', date = 'September 16, 2018', image = 'https://thumbs.dreamstime.com/b/silhouette-rock-band-9219259.jpg')
event4 = Event(name = 'Google', venue = 'Venice', description = 'CSSI', artist = 'Cssi Instructors', date = 'August 1, 2018', image = 'https://lh3.googleusercontent.com/Sz9NGQmEfK3l4UG-Iv4DRcJY8X38O2lMhxlfjM27nFZiK7MlvG_XLAFrAR3qSJzHT2DLZND56UB1R_KbOEazVpR9wEr9P6gCLtcWNtY=w1280')

events = []
events.append(event1)
events.append(event2)
events.append(event3)
events.append(event4)
current_events = Event.query().fetch()
if current_events == []:

    for i in range(len(events)):
        events[i].put()
# users = []
# user1 = User(first_name = 'DH')
# user2 = User(first_name = 'Daniel')
# user3 = User(first_name = 'Nathan')
# user4 = User(first_name = 'Sarah')
# users.append(user1)
# users.append(user2)
# users.append(user3)
# users.append(user4)
# for i in range(len(users)):
#     users[i].put()
jinja_current_directory = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# class SignUpHandler(webapp2.RequestHandler):
#     def get(self):
#         template=jinja_current_directory.get_template("templates/signup.html")
#         self.response.write(template.render())


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
                template = jinja_current_directory.get_template('templates/homepage.html')
                self.response.write(template.render({'logout_link': users.create_logout_url('/')}))
        else:
            print('not logged in')
            login_prompt_template = jinja_current_directory.get_template('templates/login.html')
            self.response.write(login_prompt_template.render({'login_link': users.create_login_url('/')}))




    #    for event in events:
    #        template_vars(event)
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
                'artist': event.artist,
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
