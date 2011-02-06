import urlparse

from zope.component import queryUtility
from zope.component import adapter

from zope.site.hooks import getSite

from zope.publisher.browser import BrowserView

from plone.registry.interfaces import IRecordModifiedEvent

from plone.dexterity.interfaces import IDexterityFTI

from plone.app.page.utils import getDefaultSiteLayout
from plone.app.page.utils import getPageSiteLayout
from plone.app.page.utils import resolveResource

from Products.CMFCore.utils import getToolByName

from plone.memoize.volatile import cache, store_on_context

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

@adapter(IRecordModifiedEvent)
def globalSiteLayoutModified(event):
    """Invalidate caches if the global site layout is changed. This will
    likely also affect things cached using plone.app.caching, which is what
    we want - the page has probably changed
    """
    if event.record.__name__ == 'plone.defaultSiteLayout':
        if event.oldValue != event.newValue:
            catalog = getToolByName(getSite(), 'portal_catalog', None)
            if catalog is not None and hasattr(catalog, '_increment_counter'):
                catalog._increment_counter()

class PageSiteLayout(BrowserView):
    """Look up and render the site layout to use for the context.
    
    Use this only for the view of a page that has the ILayout behavior
    enabled. For a more general verison, see DefaultSiteLayout below.
    
    The idea is that you can do:
    
        <link rel="layout" href="./@@page-site-layout" />
        
    and always get the correct site layout for the page, taking page- and
    section-specific settings into account.
    """
    
    @cache(cacheKey, store_on_context)
    def __call__(self):
        layout = getPageSiteLayout(self.context)
        path = urlparse.urljoin(self.context.absolute_url_path(), layout)
        return resolveResource(path)
    
class DefaultSiteLayout(BrowserView):
    """Look up and render the site layout to use for the context.
    
    Use this for a page that does not have the ILayout behavior, or a
    standalone page template.
    
    The idea is that you can do:
    
        <link rel="layout" href="./@@default-site-layout" />
        
    and always get the correct site layout for the page, taking section-
    specific settings into account.
    """
    
    @cache(cacheKey, store_on_context)
    def __call__(self):
        layout = getDefaultSiteLayout(self.context)
        path = urlparse.urljoin(self.context.absolute_url_path(), layout)
        return resolveResource(path)

