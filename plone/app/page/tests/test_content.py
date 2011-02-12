import unittest2 as unittest

from plone.app.page.testing import PAGE_INTEGRATION_TESTING

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
        