import unittest2 as unittest

from plone.app.page.testing import PAGE_INTEGRATION_TESTING

class TestUtils(unittest.TestCase):

    layer = PAGE_INTEGRATION_TESTING

    def test_getDefaultPageLayout(self):
        pass
    
    def test_getDefaultPageLayout_not_page_fti(self):
        pass
    
    def test_getPageSiteLayout(self):
        pass
    
    def test_getPageSiteLayout_not_set(self):
        pass
    
    def test_getPageTypes(self):
        pass
    
    def test_clonePageType(self):
        pass
    
    def test_clonePageType_args(self):
        pass
    
    def test_changePageType(self):
        pass
