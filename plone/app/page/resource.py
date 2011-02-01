from plone.resource.traversal import ResourceTraverser

from plone.app.page.interfaces import SITE_LAYOUT_RESOURCE_NAME
from plone.app.page.interfaces import PAGE_LAYOUT_RESOURCE_NAME

class SiteLayoutTraverser(ResourceTraverser):
    """The site layout traverser.
    
    Allows traveral to /++sitelayout++<name> using ``plone.resource`` to fetch
    things stored either on the filesystem or in the ZODB.
    """
    
    name = SITE_LAYOUT_RESOURCE_NAME

class PageLayoutTraverser(ResourceTraverser):
    """The page layout traverser.
    
    Allows traveral to /++pagelayout++<name> using ``plone.resource`` to fetch
    things stored either on the filesystem or in the ZODB.
    """
    
    name = PAGE_LAYOUT_RESOURCE_NAME
