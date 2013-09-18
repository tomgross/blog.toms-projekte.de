Migrating to Plone 4. Part 1
############################
:date: 2009-12-04 11:41
:author: Tom
:category: Plone
:tags: Plone
:slug: migrating-to-plone-4-part-1

Recently I tried to migrate the website of the `university I work for`_
to Plone 4. The first thing I did was to checkout the development
buildout from Plone
http://svn.plone.org/svn/plone/buildouts/plone-coredev/branches/4.0. The
alpha2 release is quite near, but I thought I can watch the
changes/bugfixes better, when I use the development buildout.

The next thing I did was to include our custom and third-party products
the site uses into the buildout configuration. This was the easy part,
but running the buildout gave me the first error.  It complained about
some custom packages, which were not included as development eggs. We
use the `haufe.eggserver`_ for our internal eggs and most of them were
compiled in the Python 2.4 version. I took me a while to figure out I
had to provide the 2.6 version of the eggs or the source-distributions.
*(BTW There seems to be a bug in both setuptools and distribute with the
upload command in Python 2.6. They do not accept the -r, --repository
flag and always try to upload the egg to pypi)* For that reason I chose
the source format and the eggs were recognized flawlessly.

Ready for the next step I tried to start the instance in foreground
mode. Of course there were some errors. I had to use the Plone 4
branches of  PloneFormGen and CacheFu and the the trunk of the
PloneFormGen dependencies TALESField, PythonField and TemplateFields. In
my custom products I had two errors occuring quite frequently:

#. I use safeEditProperty quite frequently. The import location changed
   from **Products.CMFPlone.migrations.migration\_util** to
   **plone.app.upgrade.utils**
#. The registerType-method of Archetypes (1.6) now takes two parameters:
   *klass* and *package*. The klass parameter has been there before. The
   package parameter is optional in Plone 3. It is the name of the
   product for packages in the Products namespace and the full name of
   the package for all others I guess.

Well now the instance with all dependencies still does not start because
of the p4a.plonecalendar, which still imports the object events from
zope.app.event. This is where I stopped today.... more to come ....

.. _university I work for: http://www.fhnw.ch
.. _haufe.eggserver: http://pypi.python.org/pypi/haufe.eggserver/
