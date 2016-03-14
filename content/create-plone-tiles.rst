Create HTML Tiles for Plone (Mosaic)
####################################
:date: 2016-03-06
:author: Tom
:category: Plone
:tags: Plone, Mosaic, Plone5, Development
:slug: create-html-tiles-for-plone-mosaic

The new kid on the block for creating flexible layouts in Plone is `plone.app.mosaic`_.
It is available for Plone 5 as an addon and will be included in a future version of core
Plone.

With the product site integrators can prepare layouts for editors to be filled with
content. The visual elements which are used by mosaic are called tiles. Tiles are
similar to viewlets, which are small HTML snippets and Python code linked to it. With
this code it is possible to access CMS data, fetch data from another database or from
a webservice. Other than viewlets tiles have a own URL.

Here I show how to easily create and register a custom tile. Let's assume we have
a custom dexterity type which carries a person record. With our tile we want to render
contact information in microformats format in a composite page.

Creating the tile
-----------------

Tiles are like all other view components in Plone registered via ZCML. A tile
configuration looks like this: ::

    <configure xmlns:plone="http://namespaces.plone.org/plone">

    <include package="plone.app.mosaic" />

    <plone:tile
        name="example.tiles.contactcard"
        title="Contact Card"
        description="A tile which displays a contact card"
        add_permission="cmf.ModifyPortalContent"
        class=".tiles.ContactCardTile"
        for="*"
        permission="zope.Public"
        schema=".tiles.IContactCardTile"
        template="templates/contact_card_tile.pt"
        />

    </configure>

The HTML template *contact_card_tile.pt* and the view class *ContactCardTile* is referenced
there.

Also we need a schema *IContactCardTile*, which is used for configuration. The only thing
we need for our schema is a reference to a contact person stored in Plone.

For our tile we can reuse plenty of code from the existingcontent tile in 
*plone.app.standardtiles*, which is also a good source for other examples.

Let's look at the schema first: ::

    from plone.app.vocabularies.catalog import CatalogSource
    from plone.supermodel import model
    from zope import schema

    class IContactCardTile(model.Schema):
       content_uid = schema.Choice(
       title=u"Select a slider object",   # XXX replace this with a message factory
       required=True,
       source=CatalogSource(portal_type=['ContactPerson',]),
       )

The schema for our contact tile is easy. It is just a reference to a *ContactPerson* object
in our database. CatalogSource takes an arbitrary catalog query as parameters. It results in
a select2 widget in edit mode for selecting a contact person.

The view class is a subclass from the ExistingContentTile without any customization ::

    from plone.app.standardtiles.existingcontent import ExistingContentTile

    class ContactCardTile(ExistingContentTile):
     """ A tile for mosaic representing a contact card """

For the template we use a simple `hCard`_ markup as a snippet ::

    <div class="vcard" tal:define="context nocall:view/content_context;">
      <a class="url fn" href="#"
         tal:attributes="href context/absolute_url"
         tal:content="context/fullname">Tom Gross</a>
    </div>

Mind the *nocall* stanza in the context define. If you don't use it, the full view
of our contact person would be called and this is not what we want.

We asume our context has a schema field named *fullname*.

We also want to test our tile, which is straight forward and can be taken almost literally
from plone.app.standardtiles. Assume you have the testing boilerplate for your product
set up with *plone.app.testing* ::

  def test_contact_card_tile(self):
        """The contact card content tile takes the uuid of a content object in the
        site and displays as a hcard template
        """

        from plone.app.mosaic.browser.tiles import ContactCardTile
        from plone.app.testing import setRoles
        from plone.app.testing import TEST_USER_ID
        setRoles(self.portal, TEST_USER_ID, ('Manager',))
        portal_url = self.portal.absolute_url()
        person_id = self.portal.invokeFactory(
            'Document', 'john-smith',
            fullname='John Smith')
        person = self.portal[person_id]
        api.content.transition(obj=person, transition='publish')
        person.reindexObject()

        person_uuid = IUUID(person)
        transaction.commit()

        tile = ContactCardTile(self.portal, self.layer['request'])

        browser = Browser(self.layer['app'])
        browser.handleErrors = False
        browser.open(
            portal_url
            + '/@@example.tiles.contactcard/unique?content_uid='
            + person_uuid)

        self.assertIn(u'John Smith', browser.contents)


Registering a tile
------------------

Now our tile is complete and tested we need to register it to use it with
plone.app.mosaic. This is done in the registry of Plone. In *registry.xml* of
the GS profile of your product. ::

    <record name="plone.app.tiles">
     <field type="plone.registry.field.List">
     <title>Tiles</title>
     <value_type type="plone.registry.field.TextLine" />
     </field>
     <value purge="false">
     <element>example.tiles.contactcard</value>
     </value>
     </record>

To display the tile in the mosaic toolbar we need the following configuration ::

    <records prefix="plone.app.mosaic.app_tiles.contact_person"
     interface="plone.app.mosaic.interfaces.ITile">
     <value key="name">example.tiles.contactcard</value>
     <value key="label">Contact Card</value>
     <value key="category">advanced</value>
     <value key="tile_type">app</value>
     <value key="default_value"></value>
     <value key="read_only">false</value>
     <value key="settings">true</value>
     <value key="favorite">false</value>
     <value key="rich_text">false</value>
     <value key="weight">20</value>
     </records>

That's all. Installing our product via the GS profile will give you a brand new
contact card tile for mosaic inclusion.

|Mosaic Tile Insert|

Have fun!

.. _plone.app.mosaic: https://github.com/plone/plone.app.mosaic
.. _hCard: markup http://microformats.org/wiki/hcard

.. |Mosaic Tile Insert| image:: static/images/contact_card_tile_insert.png
   :target: static/images/contact_card_tile_insert.png
