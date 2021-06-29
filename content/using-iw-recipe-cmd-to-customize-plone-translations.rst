Customize Plone translations with iw.recipe.cmd
###############################################
:date: 2009-07-17 14:58
:author: Tom
:category: Plone
:tags: buildout, i18n, plone
:slug: using-iw-recipe-cmd-to-customize-plone-translations
:amazon_product: placement=B0058NBIQ4&asins=B0058NBIQ4&linkId=cc39108d00358d468d6c2ab11644ba69


Sometimes the good translations of Plone do not fit your usecase or
screen space. Overriding the translations in a pre-buildout area was
easy. All you needed to do is to put a directory *i18n* in your instance
home containing a file **custom-plone-en.po**. The structure of the
filename is important: custom-DOMAIN-LANGUAGECODE.po

Nowadays all people use buildouts and adding something to the instance
doesn't seem to be a good idea. It lives in the parts directory and gets
overridden on every "install" run of buildout. A solution I use (on
Linux) is to maintain the translations in a directory *i18n* in the
buildout and let a recipe copy it to the instance.

For the recipe I use `iw.recipe.cmd`_ and the buildout snippet looks
like this:

.. code-block:: ini

 [i18n]
 recipe = iw.recipe.cmd
 on_install = true
 on_update = true
 cmds = test -d ${instance:location}/i18n && rm -rf ${instance:location}/i18n || true cp -R ${buildout:directory}/i18n ${instance:location}/

**Update! 27.08.2010**\ This Recipe only works with Plone 3. For Plone 4
and onwards it is not need any longer. The Plone i18n-domain can be
`overridden in a customization product`_.

.. _iw.recipe.cmd: http://pypi.python.org/pypi/iw.recipe.cmd/
.. _overridden in a customization product: http://article.gmane.org/gmane.comp.web.zope.plone.user/109580
