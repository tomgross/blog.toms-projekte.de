Porting tests to plone.app.testing for Plone 5
##############################################
:date: 2014-10-15
:author: Tom
:category: Plone
:tags: Plone, Testing, Plone5
:slug: porting-to-plone.app.testing

A major version of a piece of software always means to leave behind
some burdon. Plone ships with two testing framworks since Plone 4.
Now it is time to get rid of one of them: PloneTestCase.
With the newer *plone.app.testing* framework it is possible to
specify layers to encapsulate testing scenarios and dependencies.
I don't want to compete the excelent `plone.app.testing`_ documentation
here but provide some tipps for porting your addons from PloneTestCase
to plone.app.testing. 

*First*: **Look at some examples!** Most of the Plone core packages are
already ported to plone.app.testing. If you have a lot of packages
with one namespace and a similar setup it probably makes sense to
start with a ZopeSkel or `mr.bob template`_ for your `testing base class`_.

*Second*: **Use a Testing base class!** Define one or two base classes for all your
testing needs in one product. This makes migrations a lot easier.
With the help of the *PloneTestCase* class of plone.app.testing.bbb half
the work is done. All you need is a layer which installs your addon
and does the other things (create content, etc.) you need for testing.

*Third*: **Doctests** Porting doctests is a little bit more tricky. The way
doctests are run changed a little bit with plone.app.testing. You no longer
pass a testing class to the test but add a layer. This can be easily done
with the layered helper function found in plone.testing. You just pass in the
layer you defined for your unittests and you can access it in your doctests.
Because there is no test class there is no *self.<whatever-method>* supported
in doctests. Greping *'self'* in all doctests and replacing it with layer
specific code is usually the way to go.

.. code-block:: python

   >>> self.setRoles(['Manager])

would turn into

.. code-block:: python

   >>> from plone.app.testing import TEST_USER_ID, setRoles
   >>> setRoles(layer['portal'], TEST_USER_ID, ['Manager'])

And you don't need to use any Zope based variant of doctest. Just use plain python doctest and suite.

*Forth*: **Functionaltests** Basically all tests inherited from *plone.app.testing.bbb.PloneTestCase* are functional tests and support the *publish* method to publish an object in a testing environment. Sometimes I found kind of unpredictable behaviour using this method. Usually it can be avoided using zope.testbrowser (see next point). You need to use it if you are testing alternate publishing methods (like WebDAV or VirtualHostMonster) which rarly be the case.

One thing I could track down is a cookie reset if diazo is turned on. This is because of a subrequest which is issued during traversal. You can disable diazo during testing:

.. code-block:: python

  >>> response = self.publish(docpath, basic_auth, env={'diazo.off': "1"})

To debug functional testing you need the following patch in your (failing)
test.

.. code-block:: python

        def raising(self, info):
            import traceback
            traceback.print_tb(info[2])
            print info[1]

        from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
        SiteErrorLog.raising = raising

Fifth: **Testbrowser** Using zope.testbrowser is supported with
plone.app.testing too. There are two main differences: a browser instance is
initiated with the application: like this:

.. code-block:: python

   >>> browser = Browser(self.layer['app'])   # in functional test cases

or

.. code-block:: python

   >>> browser = Browser(layer['app'])    # in doctests

You need to commit changes *before!* you initiate the browser.

.. code-block:: python

   >>> from transaction import commit
   >>> commit()

Sixth: **plone.protect** 

If you are using a view, which uses CSRF protection via plone.protect you
may want to disable this feature in tests temporarily. You can call your
view by injecting a CSRF token into the request like this:

.. code-block:: python

  >>> from plone.protect import createToken
  >>> request.form['_authenticator'] = createToken()

The original idea I found in this `blog`_.

Seventh: **Functional doctests** In functional doctest sometimes a *http*
function is found. This is the doctest analog of the functional test *publish*
method. Currently it fails with plone.app.testing. I am investigating this and
keep you posted, if I found something ...

And now happy porting to plone.app.testing of your addons. BTW the porting of
some `products is left for core Plone`_. If you want to give it a try ... go ahead. :)

See you on the Plone Conference in Bristol,

Tom

.. _plone.app.testing: https://pypi.python.org/pypi/plone.app.testing
.. _blog: http://vanderwijk.info/blog/quick-hack-to-unit-test-a-browserview-that-depends-on-ploneprotect/
.. _products is left for core Plone: https://github.com/plone/Products.CMFPlone/labels/testing
.. _mr.bob template: https://github.com/FHNW/fhnw.bobtemplates/tree/master/fhnw/bobtemplates/plone_package
.. _testing base class: https://github.com/FHNW/fhnw.bobtemplates/blob/master/fhnw/bobtemplates/plone_package/src/fhnw/%2Bpackage.name%2B/tests/base.py.bob


