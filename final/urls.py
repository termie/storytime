from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'final.lasting.views.index'),
    (r'^twitter/login$', 'final.lasting.views.twitter_login'),
    (r'^twitter/callback$', 'final.lasting.views.twitter_callback'),
    (r'^choose_your_path$', 'final.lasting.views.choose_your_path'),
    #(r'^(?P<story>\s+)$', 'final.lasting.views.story'),
    #(r'^_ah/warmup$', 'final.lasting.views.warmup'),
    # Example:
    # (r'^final/', include('final.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
