==========================
My Blog @ toms-projekte.de
==========================

Go there ...

http://blog.toms-projekte.de

Build
=====

Clone from repository
 $ git clone git@github.com:tomgross/blog.toms-projekte.de.git

Get theme in submodules
 $ git submodule init
 $ git submodule update

Install Pelican blog generator
 $ pip install pelican

Generate blog
 $ pelican -t themes/pelican-bootstrap-responsive-theme/ content
