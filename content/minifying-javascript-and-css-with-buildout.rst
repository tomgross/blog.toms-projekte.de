Minifying JavaScript and CSS with buildout
##########################################
:date: 2010-02-09 14:54
:author: Tom
:tags: Multimedia, Plone
:category: Plone
:slug: minifying-javascript-and-css-with-buildout
:amazon_product: placement=B0058NBIQ4&asins=B0058NBIQ4&linkId=cc39108d00358d468d6c2ab11644ba69


An easy way to increase the performance of a web-page is to minify the
used CSS and JavaScript resources. There are ready `available tools`_
that strip the comments and whitespaces from JavaScript and CSS-files.

Plone itself ships with a big amount of uncompressed JavaScript and CSS
which are compiled in the resource registry. The usual minifying recipes
don't work in this case. To benefit from minifying resources there are
some buildout recipes, which eased my life. I recently switched to
TinyMCE, because kupu isn't compatible with IE8. TinyMCE  comes with
really many plain JavaScript-files. I believe this is true for any
(multilanguage) WYSIWYG-editor. So before putting it into production, I
minified all the resources of TinyMCE, with a striking performance
increase. What I did was changing my buildout the following way:

With the `hexagonit.recipe.download`_-recipe I download the
Java-sources of the yui-compressor

.. code-block:: ini

    [yui-compressor]
    recipe = hexagonit.recipe.download
    url = http://yuilibrary.com/downloads/yuicompressor/yuicompressor-2.4.2.zip
    strip-top-level-dir = true


The `collective.recipe.ant`_-recipe built the yui-compressor from the
previously downloaded sources for me. This recipe assumes there Java and
ant are installed and working. If ant is not in the PATH-environment,
the recipe provides the *ant-home*-option for specifying the location of
ant.

.. code-block:: ini

    [yui-compressor-build]
    recipe = collective.recipe.ant
    ant-options =
        -buildfile ${yui-compressor:location}/build.xml

Finally I used the collective.recipe.minify-recipe to add a wrapper for
minifying **ALL** resources of TinyMCE. The recipe has a *paths*-option,
where you can specify a list of paths to products, which should be
minified. The wrapper will walk these paths recursively, look for \*.css
and \*.js-files and minify them, if needed. The products don't
necessarily need to be check-outs or development-eggs. Already packaged
3rd party eggs can be walked too.

.. code-block:: ini

    [minify]
    recipe = collective.recipe.minify
    paths =
        src/Products.TinyMCE
    ignore =
    verbose = true
    include-devel = false
    css-command = java -jar ${yui-compressor:location}/build/yuicompressor-2.4.2.jar --type css
    js-command = java -jar ${yui-compressor:location}/build/yuicompressor-2.4.2.jar --type js

The full inclusion of all parts looks like this:

.. code-block:: ini

    [buildout]
    parts =
    zope2
    productdistros
    instance
    yui-compressor
    yui-compressor-build
    minify

    [yui-compressor]
    recipe = hexagonit.recipe.download
    url = http://yuilibrary.com/downloads/yuicompressor/yuicompressor-2.4.2.zip
    strip-top-level-dir = true

    [yui-compressor-build]
    recipe = collective.recipe.ant
    ant-options =
        -buildfile ${yui-compressor:location}/build.xml

    [minify]
    recipe = collective.recipe.minify
    paths =
        src/Products.TinyMCE
    ignore =
    verbose = true
    include-devel = false
    css-command = java -jar ${yui-compressor:location}/build/yuicompressor-2.4.2.jar --type css
    js-command = java -jar ${yui-compressor:location}/build/yuicompressor-2.4.2.jar --type js

    ...

After running the buildout I had a *minify*-wrapper script in the
bin-directory of my buildout. Executing it took some time (about
20minutes on my machine) and issued a

INFO: Minified 13 CSS and 917 JavaScript-files

And here is the difference:

Loading the default page of Plone in authenticated mode **without**
minified TinyMCE:

|Loading times of Plone pp|

Loading the default page of Plone in authenticated mode **with**
minified TinyMCE:

|Plone loading times minified pp|

The size of the TinyMCE-JavaScript reduced from 329.2 KB to 181.8 KB and
the loading time decreased from 523 ms to 248 ms. This is less than
half!

.. _available tools: http://developer.yahoo.com/yui/compressor/
.. _hexagonit.recipe.download: http://pypi.python.org/pypi/hexagonit.recipe.download
.. _collective.recipe.ant: http://pypi.python.org/pypi/collective.recipe.ant

.. |Loading times of Plone pp| image:: static/images/tinymce-default-3.png
   :target: static/images/tinymce-default-3.png
.. |Plone loading times minified pp| image:: static/images/tinymce-minified-3.png
   :target: static/images/tinymce-minified-3.png
