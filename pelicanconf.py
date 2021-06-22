#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Tom Gross'
SITENAME = 'Toms Blog'
SITEURL = 'https://blog.itsonsense.com'

THEME = "themes/pelican-bootstrap-responsive-theme"

TIMEZONE = 'Europe/Zurich'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ATOM = 'feeds/atom.xml'
FEED_RSS = 'feeds/rss.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = (
    ('Presenation Power', 'https://presentation-power.ch/'),
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
