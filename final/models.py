from google.appengine.ext import db


class Participant(db.Model):
  id = db.StringProperty()
  token = db.StringProperty()
  name = db.StringProperty()  # twitter name
  story = db.StringProperty()
  script = db.StringProperty()


class Story(db.Model):
  id = db.StringProperty()
  title = db.StringProperty()
  description = db.TextProperty()


class Script(db.Model):
  """The script for a given character in a story.

  Lines will be an ordered list of lines with timedeltas, with templates to
  insert the twitter names of people playing different characters.
  """
  id = db.StringProperty()
  story = db.StringProperty()
  lines = db.StringListProperty()  # format timedelta|lines
