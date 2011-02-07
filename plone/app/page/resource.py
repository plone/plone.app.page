from zope.interface import implements

from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from plone.resource.traversal import ResourceTraverser
from plone.resource.manifest import getAllResources

from plone.app.page.interfaces import SITE_LAYOUT_RESOURCE_NAME
from plone.app.page.interfaces import SITE_LAYOUT_FILE_NAME
from plone.app.page.interfaces import SITE_LAYOUT_MANIFEST_FORMAT

from plone.app.page.interfaces import PAGE_LAYOUT_RESOURCE_NAME
from plone.app.page.interfaces import PAGE_LAYOUT_FILE_NAME
from plone.app.page.interfaces import PAGE_LAYOUT_MANIFEST_FORMAT

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


class AvailableLayoutsVocabulary(object):
    """Vocabulary to return available layouts of a given type
    """
    
    implements(IVocabularyFactory)
    
    def __init__(self, format, defaultFilename):
        self.format = format
        self.defaultFilename = defaultFilename
    
    def __call__(self, context):
        items = []
        
        resources = getAllResources(self.format)
        for name, manifest in resources.items():
            title = name.capitalize().replace('-', ' ').replace('.', ' ')
            filename = self.defaultFilename
            
            if manifest is not None:
                title = manifest['title'] or title
                filename = manifest['file'] or filename
            
            path = "/++%s++%s/%s" % (self.format.resourceType, name, filename)
            items.append(SimpleTerm(path, name, title))
        
        return SimpleVocabulary(items)

AvailableSiteLayoutsVocabularyFactory = AvailableLayoutsVocabulary(
        SITE_LAYOUT_MANIFEST_FORMAT,
        SITE_LAYOUT_FILE_NAME,
    )
AvailablePageLayoutsVocabularyFactory = AvailableLayoutsVocabulary(
        PAGE_LAYOUT_MANIFEST_FORMAT,
        PAGE_LAYOUT_FILE_NAME,
    )
