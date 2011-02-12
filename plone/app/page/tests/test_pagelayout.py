import unittest2 as unittest

from plone.app.page.testing import PAGE_INTEGRATION_TESTING

class TestSiteLayout(unittest.TestCase):

    layer = PAGE_INTEGRATION_TESTING

    def test_page_site_layout(self):
        pass
    
    def test_page_site_layout_cached(self):
        pass

    def test_page_site_layout_invalidate_mtime(self):
        pass

    def test_page_site_layout_invalidate_fti_mtime(self):
        pass

    def test_page_site_layout_invalidate_registry_key(self):
        pass

    def test_page_site_layout_invalidate_catalog_counter(self):
        pass
