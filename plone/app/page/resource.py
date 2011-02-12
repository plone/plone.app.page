from zope.component import queryUtility

from plone.resource.traversal import ResourceTraverser

from plone.dexterity.interfaces import IDexterityFTI

from plone.app.blocks.resource import AvailableLayoutsVocabulary
from plone.app.blocks.resource import DefaultSiteLayout

from plone.app.page.interfaces import PAGE_LAYOUT_RESOURCE_NAME
from plone.app.page.interfaces import PAGE_LAYOUT_FILE_NAME
from plone.app.page.interfaces import PAGE_LAYOUT_MANIFEST_FORMAT

from plone.app.page.utils import getPageSiteLayout

from Products.CMFCore.utils import getToolByName

class PageLayoutTraverser(ResourceTraverser):
    """The page layout traverser.
    
    Allows traveral to /++pagelayout++<name> using ``plone.resource`` to fetch
    things stored either on the filesystem or in the ZODB.
    """
    
    name = PAGE_LAYOUT_RESOURCE_NAME

AvailablePageLayoutsVocabularyFactory = AvailableLayoutsVocabulary(
        PAGE_LAYOUT_MANIFEST_FORMAT,
        PAGE_LAYOUT_FILE_NAME,
    )

def cacheKey(method, self):
    """Invalidate if the fti is modified, the global registry is modified,
    or the content is modified
    """
    
    catalog = getToolByName(self.context, 'portal_catalog')
    fti = queryUtility(IDexterityFTI, name=self.context.portal_type)
    
    return (
            getattr(self.context, '_p_mtime', None),
            getattr(fti, '_p_mtime', None),
            catalog.getCounter(),
        )

class PageSiteLayout(DefaultSiteLayout):
    """Look up and render the site layout to use for the context.
    
    Use this only for the view of a page that has the ILayout behavior
    enabled. For a more general verison, see DefaultSiteLayout below.
    
    The idea is that you can do:
    
        <link rel="layout" href="./@@page-site-layout" />
        
    and always get the correct site layout for the page, taking page- and
    section-specific settings into account.
    """
    
    def _getLayout(self):
        return getPageSiteLayout(self.context)
