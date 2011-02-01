from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app import testing

class DecoPageLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import plone.app.page
        self.loadZCML(name='meta.zcml', package=plone.app.page)
        self.loadZCML(package=plone.app.page)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'plone.app.page:default')
        testing.setRoles(
            portal, testing.TEST_USER_ID, ['Manager', 'Member'])
        self['folder'] = portal[
            portal.invokeFactory(type_name='Folder', id='foo-folder',
                                 title='Foo Folder')]
        testing.setRoles(
            portal, testing.TEST_USER_ID, ['Member'])


DECO_PAGE_FIXTURE = DecoPageLayer()
DECO_PAGE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DECO_PAGE_FIXTURE,), name="DecoPage:Integration")
DECO_PAGE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DECO_PAGE_FIXTURE,), name="DecoPage:Functional")
