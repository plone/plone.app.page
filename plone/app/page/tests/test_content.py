import unittest2 as unittest

from plone.app.page.testing import PAGE_INTEGRATION_TESTING
from plone.app.page.testing import PAGE_FUNCTIONAL_TESTING
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser


class IntegrationTests(unittest.TestCase):

    layer = PAGE_INTEGRATION_TESTING

    def test_adding(self):

        # Ensure that invokeFactory() works as with normal types
        self.layer['folder'].invokeFactory('page', 'dp')

    def test_attributes_and_reindexing(self):
        from zope.lifecycleevent import modified

        # Demonstrate that dynamic types such as ``page``
        # automatically get the attributes specified in their model, and
        # that content is reindexed when an IObjectModified event is fired.

        folder = self.layer['folder']
        folder.invokeFactory('page', 'dp', title="Old title")
        self.assertEquals("Old title", folder['dp'].title)

        folder['dp'].title = "New Title"
        modified(folder['dp'])

        self.assertEquals("New Title", folder['dp'].title)

        results = self.layer['portal']['portal_catalog']({'Title': "New title"})
        self.assertEquals(1, len(results))

    def test_behavior_registered(self):
        from zope.component import getUtility
        from plone.behavior.interfaces import IBehavior
        from plone.app.blocks.layoutbehavior import ILayoutAware

        behavior = getUtility(IBehavior, name=u"plone.app.blocks.layoutbehavior.ILayoutAware")
        self.assertEqual(behavior.title, u'Layout support')
        self.assertEqual(behavior.interface, ILayoutAware)
        self.assertEqual(behavior.marker, ILayoutAware)

    def test_behavior_defaults(self):
        from plone.app.blocks.layoutbehavior import ILayoutAware
        
        self.layer['folder'].invokeFactory('page', 'dp')
        
        obj = self.layer['folder']['dp']
        layout = ILayoutAware(obj)
        
        self.assertEqual(layout.content, None)
        self.assertEqual(layout.pageSiteLayout, None)
        self.assertEqual(layout.sectionSiteLayout, None)
    
    def test_behavior_default_page_layout(self):
        import os.path
        
        from zope.component import provideUtility
        from zope.component import getGlobalSiteManager
        
        from plone.resource.directory import FilesystemResourceDirectory
        from plone.resource.interfaces import IResourceDirectory
        
        from plone.app.blocks.layoutbehavior import ILayoutAware
        
        basePath = os.path.dirname(__file__)
        resourcePath = os.path.join(basePath, 'resources', 'pagelayout', 'default')
        
        resourceDir = FilesystemResourceDirectory(resourcePath)
        provideUtility(resourceDir, provides=IResourceDirectory, name=u'++pagelayout++default')
        
        self.layer['folder'].invokeFactory('page', 'dp')
        
        obj = self.layer['folder']['dp']
        layout = ILayoutAware(obj)
        
        self.assertEqual(layout.content, u"<div>a page</div>")
        self.assertEqual(layout.pageSiteLayout, None)
        self.assertEqual(layout.sectionSiteLayout, None)
        
        getGlobalSiteManager().unregisterUtility(resourceDir,
                provided=IResourceDirectory,
                name=u'++pagelayout++default',
            )

    def test_page_type_has_dynamic_schema(self):
        page = self.layer['portal'].portal_types.page
        self.assertTrue(page.hasDynamicSchema)


class FunctionalTests(unittest.TestCase):

    layer = PAGE_FUNCTIONAL_TESTING

    def test_add_extra_field_to_page_type(self):
        # ensure adding extra fields works as with normal types
        browser = Browser(self.layer['app'])
        browser.addHeader('Authorization', 'Basic %s:%s' %
            (SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
        browser.open('http://nohost/plone/dexterity-types/page')
        browser.getControl('Add new field').click()
        browser.getControl('Title').value = 'Color'
        browser.getControl('Short Name').value = 'color'
        browser.getControl('Field type').value = ['Text line (String)']
        browser.getControl('Add').click()
        schema = self.layer['portal'].portal_types.page.lookupSchema()
        self.assertTrue('color' in schema.names())
        # the add view to create new instances cannot have the extra
        # field since deco doesn't work in the 'add' overlay
        browser.open('http://nohost/plone/++add++page')
        with self.assertRaises(LookupError):
            browser.getControl('Color')
        # so we first add a new instances...
        browser.getControl('Title').value = 'foo'
        browser.getControl('Save').click()
        # ...which takes us directly to the edit form,
        # where the field should be present...
        browser.getControl('Color').value = 'green'
        browser.getControl('Save').click()
        foo = self.layer['portal']['foo']
        self.assertEqual(foo.portal_type, 'page')
        self.assertEqual(foo.color, 'green')
