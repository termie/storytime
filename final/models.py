from google.appengine.ext import db


class Obituary(db.Model):
  id = db.StringProperty()
  body = db.TextProperty()
  photo = db.StringProperty()


class Story(db.Model):
  obituary = db.StringProperty()
  body = db.TextProperty()
  ordinal = db.IntegerProperty()
