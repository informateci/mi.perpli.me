#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'robeganze'
SITENAME = u'mi.perpli.me'
SITESUBTITLE = u'immagini maschie col fischio'
SITEURL = 'http://mi.perpli.me'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'it'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_DOMAIN = SITEURL
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = ()

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

ARTICLE_URL = "entries/{slug}/"
ARTICLE_SAVE_AS = "entries/{slug}/index.html"
THEME = "./vostok"

PLUGIN_PATH = "./plugins"
PLUGINS = ["slugcollision"]

STATIC_PATHS = ['extra/robots.txt', 'extra/favicon.ico', 'images']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
}
