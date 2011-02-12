from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app import testing

from zope.configuration import xmlconfig

class PageLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import plone.app.page
        self.loadZCML(name='meta.zcml', package=plone.app.page)
        self.loadZCML(package=plone.app.page)
        
        # Register directory for testing
        xmlconfig.string("""\
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="plone"
    package="plone.app.page.tests">
    
    <plone:static
        type="sitelayout"
        name="testlayout1"
        directory="resources/sitelayout/testlayout1"
        />
    
    <plone:static
        type="sitelayout"
        name="testlayout2"
        directory="resources/sitelayout/testlayout2"
        />
    
    <plone:static
        type="pagelayout"
        name="testlayout1"
        directory="resources/pagelayout/testlayout1"
        />
    
    <plone:static
        type="pagelayout"
        name="testlayout2"
        directory="resources/pagelayout/testlayout2"
        />

</configure>
""", context=configurationContext)

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

PAGE_FIXTURE = PageLayer()
PAGE_INTEGRATION_TESTING = IntegrationTesting(bases=(PAGE_FIXTURE,), name="Page:Integration")
PAGE_FUNCTIONAL_TESTING = FunctionalTesting(bases=(PAGE_FIXTURE,), name="Page:Functional")
