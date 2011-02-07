import unittest2 as unittest

from plone.app.page.testing import PAGE_INTEGRATION_TESTING

class TestTraversers(unittest.TestCase):

    layer = PAGE_INTEGRATION_TESTING

    def test_site_layout_traverser_registered(self):
        pass
    
    def test_page_layout_traverser_registered(self):
        pass

    def test_site_layouts_vocabulary(self):
        pass

    def test_page_layouts_vocabulary(self):
        pass
