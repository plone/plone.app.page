import logging
import urlparse

from zope.component import adapter
from zope.interface import implements
from zope.lifecycleevent.interfaces import IObjectAddedEvent

from plone.dexterity.content import Container
from plone.app.blocks.layoutbehavior import ILayoutAware
from plone.app.blocks.utils import resolveResource

from plone.app.page.interfaces import IPage
from plone.app.page.utils import getDefaultPageLayout

LOGGER = logging.getLogger('plone.app.page')


class Page(Container):
    """ Base class for all Page-like types.  Note that the marker interface
        must not be set on the schema, because this makes it non-dynamic) """
    implements(IPage)


@adapter(IPage, IObjectAddedEvent)
def setDefaultLayoutForNewPage(obj, event):
    """When a new page is created, set its layout based on the default in
    the FTI
    """
    
    layoutAware = ILayoutAware(obj, None)
    if layoutAware is None:
        return
    
    # Initialise object
    layoutAware.content = ILayoutAware['content'].missing_value
    layoutAware.pageSiteLayout = ILayoutAware['pageSiteLayout'].missing_value
    layoutAware.sectionSiteLayout = ILayoutAware['sectionSiteLayout'].missing_value
    
    portal_type = obj.portal_type
    template = getDefaultPageLayout(portal_type)
    
    if template is None:
        raise ValueError("Cannot find layout template for %s" % portal_type)
    
    templatePath = urlparse.urljoin(obj.absolute_url_path(), template)
    
    try:
        layoutAware.content = resolveResource(templatePath)
    except:
        LOGGER.exception("Could not resolve default page layout %s" % portal_type)
