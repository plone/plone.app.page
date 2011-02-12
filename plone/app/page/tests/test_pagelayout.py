import unittest2 as unittest

from plone.app.page.testing import PAGE_FUNCTIONAL_TESTING

class TestSiteLayout(unittest.TestCase):

    layer = PAGE_FUNCTIONAL_TESTING

    def test_page_site_layout_no_registry_key(self):
        from zope.component import getUtility
        from zope.component import getMultiAdapter
        from plone.registry.interfaces import IRegistry
        from plone.app.testing import setRoles
        from plone.app.testing import TEST_USER_ID
        from plone.app.blocks.interfaces import DEFAULT_SITE_LAYOUT_REGISTRY_KEY
        from zExceptions import NotFound
        
        portal = self.layer['portal']
        request = self.layer['request']
        
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('page', 'f1', title=u"Folder 1")
        portal['f1'].invokeFactory('page', 'p1', title=u"Page 1")
        setRoles(portal, TEST_USER_ID, ('Member',))
        
        registry = getUtility(IRegistry)
        registry[DEFAULT_SITE_LAYOUT_REGISTRY_KEY] = None
        
        view = getMultiAdapter((portal['f1']['p1'], request,), name=u'page-site-layout')
        self.assertRaises(NotFound, view)
    
    def test_page_site_layout_default(self):
        from zope.component import getUtility
        from zope.component import getMultiAdapter
        from plone.registry.interfaces import IRegistry
        from plone.app.blocks.interfaces import DEFAULT_SITE_LAYOUT_REGISTRY_KEY
        from plone.app.testing import setRoles
        from plone.app.testing import TEST_USER_ID
        
        portal = self.layer['portal']
        request = self.layer['request']
        
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('page', 'f1', title=u"Folder 1")
        portal['f1'].invokeFactory('page', 'p1', title=u"Page 1")
        setRoles(portal, TEST_USER_ID, ('Member',))
        
        registry = getUtility(IRegistry)
        registry[DEFAULT_SITE_LAYOUT_REGISTRY_KEY] = '/++sitelayout++testlayout1/site.html'
        
        view = getMultiAdapter((portal['f1']['p1'], request,), name=u'page-site-layout')
        rendered = view()
        
        self.assertTrue(u"Layout title" in rendered)

    def test_page_site_layout_page_override(self):
        from zope.component import getUtility
        from zope.component import getMultiAdapter
        from plone.registry.interfaces import IRegistry
        from plone.app.testing import setRoles
        from plone.app.testing import TEST_USER_ID
        from plone.app.blocks.layoutbehavior import ILayoutAware
        from plone.app.blocks.interfaces import DEFAULT_SITE_LAYOUT_REGISTRY_KEY
        
        portal = self.layer['portal']
        request = self.layer['request']
        
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('page', 'f1', title=u"Folder 1")
        portal['f1'].invokeFactory('page', 'p1', title=u"Page 1")
        setRoles(portal, TEST_USER_ID, ('Member',))
        
        registry = getUtility(IRegistry)
        registry[DEFAULT_SITE_LAYOUT_REGISTRY_KEY] = '/++sitelayout++testlayout1/site.html'
        
        ILayoutAware(portal['f1']['p1']).pageSiteLayout = '/++sitelayout++testlayout2/mylayout.html'
        
        view = getMultiAdapter((portal['f1']['p1'], request,), name=u'page-site-layout')
        rendered = view()
        
        self.assertFalse(u"Layout title" in rendered)
        self.assertTrue(u"Layout 2 title" in rendered)

    def test_page_site_layout_section_override(self):
        from zope.component import getUtility
        from zope.component import getMultiAdapter
        from plone.registry.interfaces import IRegistry
        from plone.app.testing import setRoles
        from plone.app.testing import TEST_USER_ID
        from plone.app.blocks.layoutbehavior import ILayoutAware
        from plone.app.blocks.interfaces import DEFAULT_SITE_LAYOUT_REGISTRY_KEY
        
        portal = self.layer['portal']
        request = self.layer['request']
        
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('page', 'f1', title=u"Folder 1")
        portal['f1'].invokeFactory('page', 'p1', title=u"Page 1")
        setRoles(portal, TEST_USER_ID, ('Member',))
        
        registry = getUtility(IRegistry)
        registry[DEFAULT_SITE_LAYOUT_REGISTRY_KEY] = '/++sitelayout++testlayout1/site.html'
        
        ILayoutAware(portal['f1']).sectionSiteLayout = '/++sitelayout++testlayout2/mylayout.html'
        
        view = getMultiAdapter((portal['f1']['p1'], request,), name=u'page-site-layout')
        rendered = view()
        
        self.assertFalse(u"Layout title" in rendered)
        self.assertTrue(u"Layout 2 title" in rendered)

    def test_page_site_layout_fti_override(self):
        from zope.component import getUtility
        from zope.component import getMultiAdapter
        from plone.registry.interfaces import IRegistry
        from plone.app.blocks.interfaces import DEFAULT_SITE_LAYOUT_REGISTRY_KEY
        from plone.app.testing import setRoles
        from plone.app.testing import TEST_USER_ID
        
        portal = self.layer['portal']
        request = self.layer['request']
        
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('page', 'f1', title=u"Folder 1")
        portal['f1'].invokeFactory('page', 'p1', title=u"Page 1")
        setRoles(portal, TEST_USER_ID, ('Member',))
        
        registry = getUtility(IRegistry)
        registry[DEFAULT_SITE_LAYOUT_REGISTRY_KEY] = '/++sitelayout++testlayout1/site.html'
        
        portal['portal_types']['page'].default_site_layout = '/++sitelayout++testlayout2/mylayout.html'
        
        view = getMultiAdapter((portal['f1']['p1'], request,), name=u'page-site-layout')
        rendered = view()
        
        self.assertFalse(u"Layout title" in rendered)
        self.assertTrue(u"Layout 2 title" in rendered)
    
    def test_page_site_layout_cache(self):
        from zope.component import getUtility
        from zope.component import getMultiAdapter
        from plone.registry.interfaces import IRegistry
        from plone.app.testing import setRoles
        from plone.app.testing import TEST_USER_ID
        from plone.app.blocks.layoutbehavior import ILayoutAware
        from plone.app.blocks.interfaces import DEFAULT_SITE_LAYOUT_REGISTRY_KEY
        
        portal = self.layer['portal']
        request = self.layer['request']
        
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('page', 'f1', title=u"Folder 1")
        portal['f1'].invokeFactory('page', 'p1', title=u"Page 1")
        setRoles(portal, TEST_USER_ID, ('Member',))
        
        registry = getUtility(IRegistry)
        registry[DEFAULT_SITE_LAYOUT_REGISTRY_KEY] = '/++sitelayout++testlayout1/site.html'
        
        ILayoutAware(portal['f1']).sectionSiteLayout = '/++sitelayout++testlayout2/mylayout.html'
        
        view = getMultiAdapter((portal['f1']['p1'], request,), name=u'page-site-layout')
        rendered = view()
        
        self.assertFalse(u"Layout title" in rendered)
        self.assertTrue(u"Layout 2 title" in rendered)
        
        # Change the section value
        ILayoutAware(portal['f1']).sectionSiteLayout = '/++sitelayout++testlayout1/site.html'
        
        view = getMultiAdapter((portal['f1']['p1'], request,), name=u'page-site-layout')
        rendered = view()
        
        # Cache means our change is ignored
        self.assertFalse(u"Layout title" in rendered)
        self.assertTrue(u"Layout 2 title" in rendered)

    def test_page_site_layout_cache_invalidate_mtime(self):
        import transaction
        from zope.component import getUtility
        from zope.component import getMultiAdapter
        from plone.registry.interfaces import IRegistry
        from plone.app.testing import setRoles
        from plone.app.testing import TEST_USER_ID
        from plone.app.blocks.layoutbehavior import ILayoutAware
        from plone.app.blocks.interfaces import DEFAULT_SITE_LAYOUT_REGISTRY_KEY
        
        portal = self.layer['portal']
        request = self.layer['request']
        
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('page', 'f1', title=u"Folder 1")
        portal['f1'].invokeFactory('page', 'p1', title=u"Page 1")
        setRoles(portal, TEST_USER_ID, ('Member',))
        
        registry = getUtility(IRegistry)
        registry[DEFAULT_SITE_LAYOUT_REGISTRY_KEY] = '/++sitelayout++testlayout1/site.html'
        
        ILayoutAware(portal['f1']).sectionSiteLayout = '/++sitelayout++testlayout2/mylayout.html'
        
        view = getMultiAdapter((portal['f1']['p1'], request,), name=u'page-site-layout')
        rendered = view()
        
        self.assertFalse(u"Layout title" in rendered)
        self.assertTrue(u"Layout 2 title" in rendered)
        
        # Trigger invalidation by changing the context
        portal['f1']['p1'].title = u"New title"
        transaction.commit()
        
        # Change the section value
        ILayoutAware(portal['f1']).sectionSiteLayout = '/++sitelayout++testlayout1/site.html'
        
        view = getMultiAdapter((portal['f1']['p1'], request,), name=u'page-site-layout')
        rendered = view()
        
        # Cache means our change is ignored
        self.assertFalse(u"Layout 2 title" in rendered)
        self.assertTrue(u"Layout title" in rendered)
    
    def test_page_site_layout_cache_invalidate_fti_mtime(self):
        import transaction
        from zope.component import getUtility
        from zope.component import getMultiAdapter
        from plone.registry.interfaces import IRegistry
        from plone.app.testing import setRoles
        from plone.app.testing import TEST_USER_ID
        from plone.app.blocks.layoutbehavior import ILayoutAware
        from plone.app.blocks.interfaces import DEFAULT_SITE_LAYOUT_REGISTRY_KEY
        
        portal = self.layer['portal']
        request = self.layer['request']
        
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('page', 'f1', title=u"Folder 1")
        portal['f1'].invokeFactory('page', 'p1', title=u"Page 1")
        setRoles(portal, TEST_USER_ID, ('Member',))
        
        registry = getUtility(IRegistry)
        registry[DEFAULT_SITE_LAYOUT_REGISTRY_KEY] = '/++sitelayout++testlayout1/site.html'
        
        ILayoutAware(portal['f1']).sectionSiteLayout = '/++sitelayout++testlayout2/mylayout.html'
        
        view = getMultiAdapter((portal['f1']['p1'], request,), name=u'page-site-layout')
        rendered = view()
        
        self.assertFalse(u"Layout title" in rendered)
        self.assertTrue(u"Layout 2 title" in rendered)
        
        # Trigger invalidation by changing the FTI
        portal['portal_types']['page'].title = u"Page type"
        transaction.commit()
        
        # Change the section value
        ILayoutAware(portal['f1']).sectionSiteLayout = '/++sitelayout++testlayout1/site.html'
        
        view = getMultiAdapter((portal['f1']['p1'], request,), name=u'page-site-layout')
        rendered = view()
        
        # Cache means our change is ignored
        self.assertFalse(u"Layout 2 title" in rendered)
        self.assertTrue(u"Layout title" in rendered)

    def test_page_site_layout_cache_invalidate_catalog_counter(self):
        from zope.component import getUtility
        from zope.component import getMultiAdapter
        from plone.registry.interfaces import IRegistry
        from plone.app.testing import setRoles
        from plone.app.testing import TEST_USER_ID
        from plone.app.blocks.layoutbehavior import ILayoutAware
        from plone.app.blocks.interfaces import DEFAULT_SITE_LAYOUT_REGISTRY_KEY
        
        portal = self.layer['portal']
        request = self.layer['request']
        
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('page', 'f1', title=u"Folder 1")
        portal['f1'].invokeFactory('page', 'p1', title=u"Page 1")
        setRoles(portal, TEST_USER_ID, ('Member',))
        
        registry = getUtility(IRegistry)
        registry[DEFAULT_SITE_LAYOUT_REGISTRY_KEY] = '/++sitelayout++testlayout1/site.html'
        
        ILayoutAware(portal['f1']).sectionSiteLayout = '/++sitelayout++testlayout2/mylayout.html'
        
        view = getMultiAdapter((portal['f1']['p1'], request,), name=u'page-site-layout')
        rendered = view()
        
        self.assertFalse(u"Layout title" in rendered)
        self.assertTrue(u"Layout 2 title" in rendered)
        
        # Trigger invalidation by incrementing the catalog counter
        portal['portal_catalog']._increment_counter()
        
        # Change the section value
        ILayoutAware(portal['f1']).sectionSiteLayout = '/++sitelayout++testlayout1/site.html'
        
        view = getMultiAdapter((portal['f1']['p1'], request,), name=u'page-site-layout')
        rendered = view()
        
        # Cache means our change is ignored
        self.assertFalse(u"Layout 2 title" in rendered)
        self.assertTrue(u"Layout title" in rendered)
    
    def test_page_site_layout_cache_invalidate_registry_key(self):
        from zope.component import getUtility
        from zope.component import getMultiAdapter
        from plone.registry.interfaces import IRegistry
        from plone.app.testing import setRoles
        from plone.app.testing import TEST_USER_ID
        from plone.app.blocks.layoutbehavior import ILayoutAware
        from plone.app.blocks.interfaces import DEFAULT_SITE_LAYOUT_REGISTRY_KEY
        
        portal = self.layer['portal']
        request = self.layer['request']
        
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('page', 'f1', title=u"Folder 1")
        portal['f1'].invokeFactory('page', 'p1', title=u"Page 1")
        setRoles(portal, TEST_USER_ID, ('Member',))
        
        registry = getUtility(IRegistry)
        registry[DEFAULT_SITE_LAYOUT_REGISTRY_KEY] = '/++sitelayout++testlayout1/site.html'
        
        ILayoutAware(portal['f1']).sectionSiteLayout = '/++sitelayout++testlayout2/mylayout.html'
        
        view = getMultiAdapter((portal['f1']['p1'], request,), name=u'page-site-layout')
        rendered = view()
        
        self.assertFalse(u"Layout title" in rendered)
        self.assertTrue(u"Layout 2 title" in rendered)
        
        # Trigger invalidation by incrementing the global registry key
        registry[DEFAULT_SITE_LAYOUT_REGISTRY_KEY] = '/++sitelayout++testlayout2/mylayout.html'
        
        # Change the section value
        ILayoutAware(portal['f1']).sectionSiteLayout = '/++sitelayout++testlayout1/site.html'
        
        view = getMultiAdapter((portal['f1']['p1'], request,), name=u'page-site-layout')
        rendered = view()
        
        # Cache means our change is ignored
        self.assertFalse(u"Layout 2 title" in rendered)
        self.assertTrue(u"Layout title" in rendered)
