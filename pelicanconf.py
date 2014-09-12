#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Tom Gross'
SITENAME = u'Toms Blog'
SITEURL = 'http://blog.toms-projekte.de'

THEME = "themes/pelican-bootstrap-responsive-theme"

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ATOM = 'feeds/atom.xml'
FEED_RSS = 'feeds/rss.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Presenation Power', 'http://presentation-power.ch/'),
          ('Plone', 'http://plone.org/'),
          )

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
DISQUS_SITENAME = "tomsblog"

PIWIK_URL = "piwik.toms-projekte.de"
PIWIK_SITE_ID = "2"
