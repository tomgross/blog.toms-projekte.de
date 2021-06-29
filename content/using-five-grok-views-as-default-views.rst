Using five.grok views as default views
######################################
:date: 2010-06-08 15:07
:author: Tom
:category: Plone
:tags: Grok, Plone
:slug: using-five-grok-views-as-default-views
:amazon_product: placement=B0058NBIQ4&asins=B0058NBIQ4&linkId=cc39108d00358d468d6c2ab11644ba69


Once you get used to the power of grok in Plone via `five.grok`_ you
never want to miss it and use it for all and everything. Unfortunately
it is currently not possible to use grok views as default views via
CMFDynamicViewFTI.

To nevertheless use them you have to do a little trick and fool
CMFDynamicViewFTI. We do so by manually adding two dummy functions to
your grok view:

.. raw:: html

   <p>

::

    class MyDefaultGrokView(grok.View):
        """ A grok view used as a default view in Plone
        """

        grok.context(MyGrokContext)

        # fix to be used with CMFDynamicViewFTI
        def __of__(self, context):
            return self

        # fix to be used with CMFDynamicViewFTI
        def __call__(self, context=None, request=None):
            return super(MyDefaultGrokView, self).__call__()

        def update(self):
            ...

No more, no less :-)

BTW My Plone book `"Plone 3 Multimedia"`_ I worked on the last year is
published and available!

.. _five.grok: http://pypi.python.org/pypi/five.grok/
.. _"Plone 3 Multimedia": http://amzn.to/dtrp0C
