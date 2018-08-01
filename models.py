from google.appengine.ext import ndb

class User(ndb.Model):
    first_name =  ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    #email_address = ndb.StringProperty(required = True)
    id = ndb.StringProperty(required=True)
    #gender = ndb.StringProperty(required=False)

    # address = ndb.StringProperty(required=False)

#One to One
class Event(ndb.Model):

    name = ndb.StringProperty(required=True)
    venue = ndb.StringProperty(required=True)
    artist = ndb.StringProperty(required=True)
    date = ndb.StringProperty(required=True)
    # time_start = ndb.DateTimeProperty(required=True)
    # time_end = ndb.DateTimeProperty(required=True)
    description = ndb.StringProperty(required=True)
    image = ndb.StringProperty(required=True)

class UserEvent(ndb.Model):
    user_key = ndb.KeyProperty(User)
    event_key = ndb.KeyProperty(Event)

#class Forum(ndb.Model):


    #
    # top_text = ndb.StringProperty(required=False)
    # bottom_text = ndb.StringProperty(required=False)
    # template = ndb.KeyProperty(Template)
    # creator = ndb.StringProperty(required=True)
    # created_at = ndb.DateTimeProperty(required=True)
