Stumbling upon TextIndexNG3s ranking features
#############################################
:date: 2011-05-25 08:52
:author: Tom
:tags: Index, Plone
:category: Plone
:slug: stumbling-upon-textindexng3s-ranking-features
:amazon_product: placement=B0058NBIQ4&asins=B0058NBIQ4&linkId=cc39108d00358d468d6c2ab11644ba69


For a Plone site I use `TextIndexNG3`_ for the fulltext index with the
ranking support (*txng.ranking.cosine*) turned on. Searching content
worked fine on the development box but when transferred to the live box,
some mysterious things happened. Some of the documents were not found
and strangely with the same words than on the development box. The first
suspicion was a encoding issue but this turned out to be wrong.
Some documents with common words (like "Änderung" - a german word
meaning "changes") were not found in a query like this:

.. code-block:: python
 
 >>> q = {'portal_type':('News Item',),
 ...      'SearchableText':unicode('änderungen', 'utf-8')}
 >>> r = cat.searchResults(**q)

Other documents with the same query but less common or nonsense words are found. Like this:

.. code-block:: python

 >>> q = {'portal_type':('News Item',),
 ...      'SearchableText':unicode('änderüngen', 'utf-8')}
 >>> r = cat.searchResults(**q)

Inspecting the code of the index revealed the problem. There is a
limit (50 items) for ranked results in the index! Later I found the
limit is documented on the pypi-page of TextIndexNG3, but I didn't
expect the Index to work like this. On the development box there were to
few data to reach the limit and on the live box the limit is applied to
**all** contents of the fulltext index, not only the requested subset of
news items. The problem was solved by turning of the ranking on query
basis. Like this:

.. code-block:: python
 
 >>> q = {'portal_type':('News Item',),
 ...      'SearchableText':{'query':unicode('änderungen', 'utf-8'),
 ...                        'ranking':False}}
 >>> r = cat.searchResults(**q)

or specifying a sufficient high number of *ranking\_maxhits*. Like this:

.. code-block:: python
 
 >>> q = {'portal_type':('News Item',),
 ...      'SearchableText':{'query':unicode('änderungen', 'utf-8'),
                            'ranking':True, 'ranking_maxhits':20000}}
 >>> r = cat.searchResults(**q)

A "sufficient high number" would be the number of objects stored in your catalog.

Hope this keeps someone of looking for the needle in the haystack for
hours, like I did.

.. _TextIndexNG3: http://pypi.python.org/pypi/Products.TextIndexNG3/
