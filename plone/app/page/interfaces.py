from zope.interface import Interface
from zope import schema

from plone.resource.manifest import ManifestFormat

from plone.dexterity.interfaces import IDexterityFTI

from plone.app.page import PloneMessageFactory as _

DEFAULT_PAGE_TYPE_NAME = "page"

PAGE_LAYOUT_RESOURCE_NAME = "pagelayout"
PAGE_LAYOUT_FILE_NAME = "page.html"

PAGE_LAYOUT_MANIFEST_FORMAT = ManifestFormat(PAGE_LAYOUT_RESOURCE_NAME,
        keys=('title', 'description', 'file'),
        defaults={'file': PAGE_LAYOUT_FILE_NAME},
    )

class IPage(Interface):
    """The page type
    """

class IPageFTI(IDexterityFTI):
    """Page factory type information.
    
    This serves three purposes:
    
    * Set up defaults applicable to the page content type
    * Add properties to store the default site layout and page layout template
    * Provide a primitive that can be used to manage page categories (which
      are implemented as FTIs)
    """
    
    default_site_layout = schema.Choice(
            title=_(u"Default site layout"),
            description=_(u"The default site layout used when creating new pages of this type"),
            vocabulary='plone.availableSiteLayouts',
        )
    
    default_page_layout_template = schema.Choice(
            title=_(u"Default page layout template"),
            description=_(u"The default page layout template used when creating new pages of this type"),
            vocabulary='plone.availablePageLayouts',
        )
