import uuid

from final import models


def create_participant(user_info):
  name = user_info.get('username')
  token = user_info.get('token')
  secret = user_info.get('secret')
  id = str(user_info.get('id'))

  p = models.Participant(key_name=name,
                         id=id,
                         name=name,
                         token=token,
                         secret=secret)
  p.save()
  return p


def get_participant(key_name):
  return models.Participant.get_by_key_name(key_name)


def list_stories():
  return models.Story.all()
