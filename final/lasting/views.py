import json
import random

from django import http
from django import template
from django import shortcuts
from django.conf import settings
from django.template import loader

from google.appengine.api import memcache
from google.appengine.ext import db

from final import api
from final import models
from final import oauth


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
  #obituarys = _get_data()
  #random.shuffle(obituarys)
  # Don't show photos for those without statements.
  #obituarys = [x for x in obituarys
  #             if x.photo and x.statement != DECLINED]
  # Or do
  #obituarys = [x for x in obituarys
  #             if x.photo or x.statement != DECLINED]
  return shortcuts.render_to_response('templates/index.html', locals())


def twitter_login(request):
  client = oauth.TwitterClient(settings.TWITTER_CONSUMER,
                               settings.TWITTER_SECRET,
                               settings.TWITTER_CALLBACK)
  return shortcuts.redirect(client.get_authorization_url())


def twitter_callback(request):
  client = oauth.TwitterClient(settings.TWITTER_CONSUMER,
                               settings.TWITTER_SECRET,
                               settings.TWITTER_CALLBACK)
  auth_token = request.REQUEST.get('oauth_token')
  auth_verifier = request.REQUEST.get('oauth_verifier')
  user_info = client.get_user_info(auth_token, auth_verifier=auth_verifier)

  p = api.create_participant(user_info)
  request.session['user'] = p.key().name()
  return shortcuts.redirect('/pick_a_story')


def pick_a_story(request):
  # TODO(termie): move this into an auth middleware on the request
  user = api.get_participant(request.session.get('user'))
  return shortcuts.render_to_response('templates/pick_a_story.html', locals())


def individual(request, id):
  obituarys = [_get_single(id)]
  return shortcuts.render_to_response('templates/individual.html', locals())
