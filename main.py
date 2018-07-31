import json
import webapp2
import os
import jinja2
import random

from models import User, Event
from google.appengine.api import users






jinja_current_directory = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class StartHandler(webapp2.RequestHandler):
    def get(self):
        template=jinja_current_directory.get_template("templates/start.html")
        self.response.write(template.render())


class SignUpHandler(webapp2.RequestHandler):
    def get(self):
        template=jinja_current_directory.get_template("templates/signup.html")
        self.response.write(template.render())

class LogInHandler(webapp2.RequestHandler):

    pass
class HomePageHandler(webapp2.RequestHandler):
    def get(self):
        template_vars ={

        }
        self.response.write('hello')
    #    for event in events:
    #        template_vars(event)
    def post(self):
        pass

class GroupPageHandler(webapp2.RequestHandler):
    def post(self):
        event_key = self.request.get('event_chosen')
        UserEvents = UserEvent.query().filter(UserEvent.event_key == event_key)
        UserList = []
        for i in range(len(UserEvents)):
            user_key = UserEvents[i].user_key
            user = user_key.get()
            UserList.append(user)


# class MemeBrowser(webapp2.RequestHandler):
#     def get(self):
#         memes = Meme.query().order(-Meme.created_at).fetch(10)
#         for meme in memes:
#             meme.template_filename = meme.template.get().image_file
#         start_template=jinja_current_directory.get_template("templates/latestmemes.html")
#         self.response.write(start_template.render({'memes': memes}))
#
# class AddMemeHandler(webapp2.RequestHandler):
#     def get(self):
#         templates = Template.query().fetch()
#         add_template=jinja_current_directory.get_template("templates/new_meme.html")
#         self.response.write(add_template.render({'templates': templates}))
#
#     def post(self):
#         user = users.get_current_user()
#         template_name = self.request.get('template')
#         template_key = Template.query(Template.name == template_name).fetch(1)[0].key
#         Meme(top_text=self.request.get('top_text'),
#              bottom_text=self.request.get('bottom_text'),
#              template=template_key,
#              creator=user.email(),
#              created_at=datetime.datetime.utcnow()).put()
#         self.redirect('/')
#



app = webapp2.WSGIApplication([
    ('/', StartHandler),
    ('/login', LogInHandler),
    ('/signup', SignUpHandler),
    ('/homepage', HomePageHandler)
], debug=True)
