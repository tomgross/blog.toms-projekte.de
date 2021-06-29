Workaround setuptools 8.0 bug with zc.buildout
##############################################
:date: 2014-12-13
:author: Tom
:category: Plone
:tags: Plone, setuptools, workaround
:slug: workaround-setuptools-buildout-bug
:amazon_product: placement=B0058NBIQ4&asins=B0058NBIQ4&linkId=cc39108d00358d468d6c2ab11644ba69


Buildout always fetches the latest version of setuptools
for bootstraping. No matter what is defined in versions.cfg.
It is possible to set the version of zc.buildout when
bootstraping but not the one of setuptools.

This behavior is hardcoded in `bootstrap.py`.

.. code-block:: python

  77 ez = {}
  78 exec(urlopen('https://bootstrap.pypa.io/ez_setup.py'
  79             ).read(), ez)
  80 if not options.allow_site_packages:

Unfortunately there are some incompatible changes (a bug?)
in setuptools 8.0 which prevent zc.buildout from bootstraping.
It fails with the following error:

.. code-block:: bash

  tom@localhost:~/demobuildout> python2.7 bootstrap.py 
  Downloading https://pypi.python.org/packages/source/s/setuptools/setuptools-8.0.zip
  Extracting in /tmp/tmp_34LbA
  Now working in /tmp/tmp_34LbA/setuptools-8.0
  Building a Setuptools egg in /tmp/tmpeA5PHB
  /tmp/tmpeA5PHB/setuptools-8.0-py2.7.egg
  Traceback (most recent call last):
    File "bootstrap.py", line 145, in <module>
      if _final_version(distv):
    File "bootstrap.py", line 131, in _final_version
      for part in parsed_version:
  TypeError: 'Version' object is not iterable

I found a quite easy workaround to use a different version
of setuptools until this issue is fixed. Setuptools 7.0 seems
to work fine. Do the following:

 1. Create a directory and change to it::

    $ mkdir setuptools-workaround
    $ cd setuptools-workaround 

 2. Download `ez_setup.py`::

    $ wget https://bootstrap.pypa.io/ez_setup.py

 3. Edit `ez_setup.py` and change the setuptools version to be used.::

     39 DEFAULT_VERSION = "7.0"
     40 DEFAULT_URL = "https://pypi.python.org/packages/source/s/setuptools/"

 4. Start a python webserver in the directory.::

     $ python -m SimpleHTTPServer

    The server does not daemonize itself. The following actions need to be done in a
    new terminal.

 5. Now change the line where it downloads ez_setup.py in your
    bootstrap.py file to use the patched ez_setup.py.

.. code-block:: python

     77 ez = {}
     78 exec(urlopen('http://localhost:8000/ez_setup.py'
     79             ).read(), ez)
     80 if not options.allow_site_packages:

 6. You are ready to start your working buildout.

.. code-block:: bash

     tom@linux-zoc2:~/demobuildout> python bootstrap.py 
     Downloading https://pypi.python.org/packages/source/s/setuptools/setuptools-7.0.zip
     Extracting in /tmp/tmp82Jp3m
     Now working in /tmp/tmp82Jp3m/setuptools-7.0
     Building a Setuptools egg in /tmp/tmpgDuB3k
     /tmp/tmpgDuB3k/setuptools-7.0-py2.7.egg
     Generated script '/home/tom/demobuildout/bin/buildout'.

This works for me. Hope this bug is fixed soon anyway.
