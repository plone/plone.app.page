import unittest
import plone.app.page

from zope.component import getMultiAdapter

from zope.lifecycleevent import modified

from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup


@onsetup
def setup_product():
    zcml.load_config('meta.zcml', plone.app.page)
    zcml.load_config('configure.zcml', plone.app.page)

setup_product()
ptc.setupPloneSite(products=['plone.app.page'])


class IntegrationTests(ptc.PloneTestCase):

    def test_adding(self):

        # Ensure that invokeFactory() works as with normal types

        self.folder.invokeFactory('plone.app.page', 'dp')

    def test_attributes_and_reindexing(self):

        # Demonstrate that dynamic types such as plone.page
        # automatically get the attributes specified in their model, and
        # that content is reindexed when an IObjectModified event is fired.

        self.folder.invokeFactory('plone.app.page', 'dp', title="Old title")
        self.assertEquals("Old title", self.folder.dp.title)

        self.folder.dp.title = "New Title"
        modified(self.folder.dp)

        self.assertEquals("New Title", self.folder.dp.title)

        results = self.portal.portal_catalog(Title="New title")
        self.assertEquals(1, len(results))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(IntegrationTests))
    return suite
