import unittest2 as unittest

from plone.app.page.testing import PAGE_INTEGRATION_TESTING

class TestUtils(unittest.TestCase):

    layer = PAGE_INTEGRATION_TESTING

    def test_clonePageType(self):
        from plone.app.page.utils import clonePageType
        
        portal = self.layer['portal']
        portal_types = portal['portal_types']
        oldFTI = portal_types['page']
        
        self.assertFalse('new-page' in portal_types)
        
        clonePageType(portal_types, 'page', 'new-page', u"New page", "A new page type")
        newFTI = portal_types['new-page']
        
        self.assertEqual(newFTI.title, u"New page")
        self.assertEqual(newFTI.description, u"A new page type")
        self.assertEqual(newFTI.add_view_expr, 'string:${folder_url}/++add++new-page')
        
        self.assertEqual(newFTI.immediate_view, oldFTI.immediate_view)
        self.assertEqual(newFTI.klass, oldFTI.klass)
        self.assertEqual(newFTI.schema, oldFTI.schema)
        self.assertEqual(newFTI.behaviors, oldFTI.behaviors)
        self.assertEqual(newFTI.default_site_layout, oldFTI.default_site_layout)
        self.assertEqual(newFTI.default_page_layout_template, oldFTI.default_page_layout_template)
    
    def test_clonePageType_args(self):
        from plone.app.page.utils import clonePageType
        
        portal = self.layer['portal']
        portal_types = portal['portal_types']
        oldFTI = portal_types['page']
        
        self.assertFalse('new-page' in portal_types)
        
        clonePageType(portal_types, 'page', 'new-page', u"New page", "A new page type",
            default_site_layout="/++sitelayout++testlayout2/mylayout.html")
        newFTI = portal_types['new-page']
        
        self.assertEqual(newFTI.title, u"New page")
        self.assertEqual(newFTI.description, u"A new page type")
        self.assertEqual(newFTI.add_view_expr, 'string:${folder_url}/++add++new-page')
        
        self.assertEqual(newFTI.immediate_view, oldFTI.immediate_view)
        self.assertEqual(newFTI.klass, oldFTI.klass)
        self.assertEqual(newFTI.schema, oldFTI.schema)
        self.assertEqual(newFTI.behaviors, oldFTI.behaviors)
        self.assertEqual(newFTI.default_site_layout, "/++sitelayout++testlayout2/mylayout.html")
        self.assertEqual(newFTI.default_page_layout_template, oldFTI.default_page_layout_template)
    
    def test_getPageTypes(self):
        from plone.app.page.utils import clonePageType
        from plone.app.page.utils import getPageTypes
        
        portal = self.layer['portal']
        portal_types = portal['portal_types']
        
        clonePageType(portal_types, 'page', 'new-page', u"New page", "A new page type")
        
        pageTypes = getPageTypes(portal_types)
        ids = sorted([p.getId() for p in pageTypes])
        
        self.assertEqual(ids, ['new-page', 'page'])
    
    def test_changePageType(self):
        from plone.app.page.utils import clonePageType
        from plone.app.page.utils import changePageType
        from plone.app.testing import TEST_USER_ID
        from plone.app.testing import setRoles
        
        portal = self.layer['portal']
        portal_types = portal['portal_types']
        
        clonePageType(portal_types, 'page', 'new-page', u"New page", "A new page type")
        
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('page', 'p1', title=u"A page")
        setRoles(portal, TEST_USER_ID, ('Member',))
        
        self.assertEqual(portal['p1'].portal_type, 'page')
        
        changePageType(portal['p1'], 'new-page')
        
        self.assertEqual(portal['p1'].portal_type, 'new-page')
    
    def test_createTemplatePageLayout(self):
        from plone.app.page.interfaces import PAGE_LAYOUT_MANIFEST_FORMAT
        from plone.app.page.utils import createTemplatePageLayout
        
        from plone.resource.utils import queryResourceDirectory
        from plone.resource.manifest import getManifest
        
        from plone.app.testing import TEST_USER_ID
        from plone.app.testing import setRoles
        
        portal = self.layer['portal']
        
        setRoles(portal, TEST_USER_ID, ('Manager',))
        createTemplatePageLayout(u"A title", u"A description", u"<html><body><p>Stuff</p></body></html>")
        setRoles(portal, TEST_USER_ID, ('Member',))
        
        directory = queryResourceDirectory('pagelayout', 'a-title')
        
        self.assertTrue('page.html' in directory)
        self.assertTrue('manifest.cfg' in directory)
        self.assertEqual(directory.readFile('page.html'), "<html><body><p>Stuff</p></body></html>")
        
        manifest = getManifest(directory.openFile('manifest.cfg'), PAGE_LAYOUT_MANIFEST_FORMAT)
        self.assertEqual(manifest, {'title': "A title", 'description': "A description", 'file': 'page.html'})
        
        # Create a second one with the same title
        
        setRoles(portal, TEST_USER_ID, ('Manager',))
        createTemplatePageLayout(u"A title", u"Another description", u"<html><body><p>Other stuff</p></body></html>")
        setRoles(portal, TEST_USER_ID, ('Member',))
        
        directory = queryResourceDirectory('pagelayout', 'a-title-1')
        
        self.assertTrue('page.html' in directory)
        self.assertTrue('manifest.cfg' in directory)
        self.assertEqual(directory.readFile('page.html'), "<html><body><p>Other stuff</p></body></html>")
        
        manifest = getManifest(directory.openFile('manifest.cfg'), PAGE_LAYOUT_MANIFEST_FORMAT)
        self.assertEqual(manifest, {'title': "A title", 'description': "Another description", 'file': 'page.html'})
        