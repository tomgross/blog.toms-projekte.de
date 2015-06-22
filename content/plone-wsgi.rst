Run Plone 5 with WSGI
#####################
:date: 2015-06-22
:author: Tom
:category: Plone
:tags: Plone, WSGI, Plone5, Deployment
:slug: run-plone-with-wsgi

Now Zope has `documented`_ support of WSGI deployment, Plone can have it too.
To make it happen we can use a minimal buildout with some minor adjustments: ::

 [buildout]
 parts = instance
 extends = http://dist.plone.org/release/5-latest/versions.cfg

 [instance]
 recipe = plone.recipe.zope2instance
 http-address =
 eggs =
   Plone
   Pillow

 [wsgiconf]
 recipe = collective.recipe.template
 input = zope.wsgi.in
 output = zope.wsgi

 [app]
 recipe = zc.recipe.egg
 eggs =
   ${instance:eggs}
   repoze.who
   repoze.tm2
   repoze.retry
   Paste
   PasteScript
   PasteDeploy


**Note the empty `http-address` in the instance-recipe.** We specify host and port
in the WSGI configuration which is generated with the `wsgiconf` recipe.

This is an example for a simple WSGI deployment. It contains a Paste server listening
on port 8080. Content is served from Zope for all URLs except /static, which comes
from the directory called `static` and lives in the var-direcory of the buildout.

With this buildout you need to take care of creating it yourself. But this shouldn't
be to hard with the `collective.recipe.cmd`_ recipe.

Now here is the WSGI config: ::

 [app:zope-app]
 use = egg:Zope2#main
 zope_conf = ${instance:location}/etc/zope.conf

 [pipeline:zope-pipeline]
 pipeline =
    egg:paste#evalerror
    egg:repoze.retry#retry
    egg:repoze.tm2#tm
    zope-app

 [app:static]
 use = egg:Paste#static
 document_root = ${buildout:directory}/var/static

 [composite:main]
 use = egg:Paste#urlmap
 / = zope-pipeline
 /static = static

 [server:main]
 use = egg:paste#http
 host = localhost
 port = 8080

The complete configuration files you can find in this `gist`_

After running the buildout and start the instance with: ::

 $ bin/paster serve zope.wsgi

Have fun with a fresh Plone 5 instance :-)

|Plone 5 WSGI Startpage|

You can put static HTML, CSS and JavaScript in the static
directory and accessing it directly.

|Plone 5 WSGI Helloworld|

.. _collective.recipe.cmd: https://pypi.python.org/pypi/collective.recipe.cmd/0.11
.. _gist: https://gist.github.com/tomgross/160e17486a6e038f6f61
.. _documented: https://github.com/zopefoundation/Zope/pull/32

.. |Plone 5 WSGI Startpage| image:: static/images/wsgi-plone.png
   :target: static/images/wsgi-plone.png
.. |Plone 5 WSGI Helloworld| image:: static/images/wsgi-helloworld.png
   :target: static/images/wsgi-helloworld.png
