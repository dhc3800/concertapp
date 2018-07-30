from google.appengine.ext import ndb

class User(ndb.Model):
    first_name =  ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    email_address = ndb.StringProperty(required = True)


#One to One
class Event(ndb.Model):

    name = ndb.StringProperty(required=True)
    address = ndb.StringProperty(required=True)
    date = ndb.DateProperty(required=True)
    time_start = ndb.DateTimeProperty(required=True)
    time_end = ndb.DateTimeProperty(required=True)

class Relation(ndb.Model):
    user_key = ndb.KeyProperty(User)
    event_key = ndb.KeyProperty(Event)

#class Forum(ndb.Model):

    #
    # top_text = ndb.StringProperty(required=False)
    # bottom_text = ndb.StringProperty(required=False)
    # template = ndb.KeyProperty(Template)
    # creator = ndb.StringProperty(required=True)
    # created_at = ndb.DateTimeProperty(required=True)
