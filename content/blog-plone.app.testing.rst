Title: Porting tests to plone.app.testing for Plone 5
Date: 2014-09-25

A major version of a piece of software always means to leave behind
some burdon. Plone ships with two testing framworks since Plone 4.
Now it is time to get rid of one of them: PloneTestCase.
With the newer **plone.app.testing** framework it is possible to
specify layers to encapsulate testing scenarios and dependencies.
I don't want to compete the excelent **plone.app.testing** documentation
here but provide some tipps for porting your addons from PloneTestCase
to plone.app.testing. 

First: Look at some examples. Most of the Plone core packages are
already ported to plone.app.testing. If you have a lot of packages
with one namespace and a similar setup it probably makes sense to
start with a ZopeSkel or mr.bob template for your testing base class.

Second: Testing base class. Define one or two base classes for all your
testing needs in one product. This makes migrations a lot easier.
plone.app.testing.bbb

Third: Porting doctests is a little bit more tricky. First

grep self
use plain python doctest
use layered function

Forth: functionaltests with publish

Fivth: Using zope.testbrowser is supported with plone.app.testing too.
There are two main differences: a browser instance is initiated with the
application: like this

   >>> browser = Browser(self.layer['app'])   # in functional test cases

or
  
   >>> browser = Browser(layer['app'])    # in doctests

You need to commit changes *before!* you initiate the browser.

   >>> from transaction import commit
   >>> commit()


6: plone.protect

7: publish method of ZopeTestCase.functional

   be careful with diazo (see tests of Products.PloneLanguagTool) it uses
   a subrequest

        def raising(self, info):
            import traceback
            traceback.print_tb(info[2])
            print info[1]

        from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
        SiteErrorLog.raising = raising

   http call in functional doctest


