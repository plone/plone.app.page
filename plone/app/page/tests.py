import unittest2 as unittest
import doctest

from zope.component import getMultiAdapter

from zope.lifecycleevent import modified

from plone.app.page import testing

OPTIONFLAGS = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE


class IntegrationTests(unittest.TestCase):

    layer = testing.DECO_PAGE_INTEGRATION_TESTING

    def test_adding(self):

        # Ensure that invokeFactory() works as with normal types

        self.layer['folder'].invokeFactory('plone.app.page', 'dp')

    def test_attributes_and_reindexing(self):

        # Demonstrate that dynamic types such as plone.page
        # automatically get the attributes specified in their model, and
        # that content is reindexed when an IObjectModified event is fired.

        folder = self.layer['folder']
        folder.invokeFactory('plone.app.page', 'dp', title="Old title")
        self.assertEquals("Old title", folder.dp.title)

        folder.dp.title = "New Title"
        modified(folder.dp)

        self.assertEquals("New Title", folder.dp.title)

        results = self.layer['portal'].portal_catalog(Title="New title")
        self.assertEquals(1, len(results))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(IntegrationTests))
    return suite
