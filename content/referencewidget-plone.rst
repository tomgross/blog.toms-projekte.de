Using archetypes.referencebrowserwidget with Plone 3.3
######################################################
:date: 2009-04-23 08:18
:author: Tom
:category: Plone
:tags: Archetypes, Plone, Referencebrowser, Widget
:slug: referencewidget-plone

If you need to reference objects from big containers, the current
ATReferenceBrowser product, which is bundled with Plone may not be your
first choice. It is very slow with many objects and it is not very well
tested, if at all. The at.referencebrowserwidget aims to be 100% UI
compatible but using modern components in the background and there
should be tests for all the features it provides. Well, and here it is.
It is not finished yet but it works and is used in some productive
environments.

You can include it like any other product in your buildout ::

 [buildout] 
 ... 
 eggs = 
   ... 
   archetypes.referencebrowserwidget
  
 [instance]
 ... 
 zcml = 
   ...
   archetypes.referencebrowserwidget 
 ...

This will enable it for being installed via quickinstaller. If you do so
the skin of ATReferenceBrowserWidget gets overridden by the one of
archetypes.referencebrowserwidget. This means the widget code is still
ATRefernceBrowserWidget, but the popup and everything behind it is
archetypes.referencebrowserwidget.

But you can have more, if you want (and using Plone >= 3.2 and < 4.0).

There is a replacement of ATReferenceBrowserWidget, which can be used
as stub to satisfy current dependencies on import location and names.
You can find it here:

http://svn.plone.org/svn/archetypes/MoreFieldsAndWidgets/ATReferenceBrowserWidget/branches/tom_gross_skeletononly/

named "*Products.ATReferenceBrowserWidget" * in the
"*src*"-directory of your buildout. And change the *buildout.cfg* to
the following: ::

 [buildout]
 ...
 develop = src/Products.ATReferenceBrowserWidget
 
 [versions]
 Products.ATReferenceBrowserWidget = 3.0-withatref
 
 [instance]
 ...
 eggs = 
   ${buildout:eggs}
   Plone
   archetypes.referencebrowserwidget
 ...

That's it. This will enable you the full power of the new widget. Have fun!
