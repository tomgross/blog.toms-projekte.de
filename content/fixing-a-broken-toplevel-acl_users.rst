Fixing a broken toplevel acl_users 
###################################
:date: 2013-03-25 14:07
:author: Tom
:category: Plone
:tags: Plone, Authentication
:slug: fixing-a-broken-toplevel-acl_users

Sometimes someone forgets his admin password. This is easy to reset with
the adduser command of Zope. But what if someone removes the top level
ZODB user manager? Use this commands to restore it in debug mode:

Start instance in debug mode:

::

 $ bin/instance debug

Add a new ZODB user manager and activate necessary plugins:
 
>>> from Products.PluggableAuthService.plugins.ZODBUserManager import addZODBUserManager
>>> addZODBUserManager(app.acl_users, 'users')
>>> from Products.PluggableAuthService.interfaces.plugins import IUserEnumerationPlugin
>>> from Products.PluggableAuthService.interfaces.plugins import IUserAdderPlugin
>>> from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin
>>> app.acl_users.plugins.activatePlugin(IUserEnumerationPlugin, 'users')
>>> app.acl_users.plugins.activatePlugin(IUserAdderPlugin, 'users')
>>> app.acl_users.plugins.activatePlugin(IAuthenticationPlugin, 'users')
>>> import transaction
>>> transaction.commit()

Add a new management user:

::

  $ bin/instance adduser admin admin

Start the instance and go to ZMI and change the password of the admin
user!
