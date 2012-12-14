import random

from django import template
from django import shortcuts
from django.template import loader

from google.appengine.api import memcache
from google.appengine.ext import db

from final import models


DECLINED = 'This obituary declined to make a last statement.'


def _get_data():
  data = memcache.get("shown_obituarys")
  if data is not None:
    return data
  else:
    #obituarys = db.GqlQuery('SELECT photo, statement, name_first, name_last, '
    #                        '       age, county '
    #                        'FROM Obituary '
    #                        'WHERE show = True '
    #                        'ORDER BY number ')
    obituarys = db.GqlQuery('SELECT * '
                            'FROM Obituary '
                            'WHERE show = True '
                            'ORDER BY number ')
    obituarys = list(obituarys)
    memcache.add("shown_obituarys", obituarys)
    return obituarys


def _get_single(id):
  data = memcache.get("obituary_%s" % id)
  if data is not None:
    return data
  else:
    obituary = models.Obituary.get_by_key_name(str(id))
    stories = models.Story.all().filter('obituary = %s')
    memcache.add("obituary_%s" % id, obituary)
    return obituary


def index(request):
  #t = loader.get_template('templates/index.html')
  #c = template.RequestContext(request, locals())
  obituarys = _get_data()
  random.shuffle(obituarys)
  # Don't show photos for those without statements.
  #obituarys = [x for x in obituarys
  #             if x.photo and x.statement != DECLINED]
  # Or do
  #obituarys = [x for x in obituarys
  #             if x.photo or x.statement != DECLINED]
  return shortcuts.render_to_response('templates/index.html', locals())


def individual(request, id):
  obituarys = [_get_single(id)]
  return shortcuts.render_to_response('templates/individual.html', locals())
