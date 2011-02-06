from zope.interface import Interface
from zope import schema

from plone.dexterity.interfaces import IDexterityFTI
from plone.resource.manifest import ManifestFormat

from plone.app.page import PloneMessageFactory as _

SITE_LAYOUT_RESOURCE_NAME = "sitelayout"
SITE_LAYOUT_FILE_NAME = "site.html"

PAGE_LAYOUT_RESOURCE_NAME = "pagelayout"
PAGE_LAYOUT_FILE_NAME = "page.html"

SITE_LAYOUT_MANIFEST_FORMAT = ManifestFormat(SITE_LAYOUT_RESOURCE_NAME,
        keys=('title', 'description', 'file'),
        defaults={'file': 'site.html'},
    )
PAGE_LAYOUT_MANIFEST_FORMAT = ManifestFormat(PAGE_LAYOUT_RESOURCE_NAME,
        keys=('title', 'description', 'file'),
        defaults={'file': 'page.html'},
    )

class IPageFTI(IDexterityFTI):
    """Page factory type information.
    
    This serves three purposes:
    
    * Set up defaults applicable to the page content type
    * Add properties to store the default site layout and page layout template
    * Provide a primitive that can be used to manage page categories (which
      are implemented as FTIs)
    """
    
    default_site_layout = schema.ASCIILine(
            title=_(u"Default site layout"),
            description=_(u"The default site layout used when creating new pages of this type"),
        )
    
    default_page_layout_template = schema.ASCIILine(
            title=_(u"Default page layout template"),
            description=_(u"The default page layout template used when creating new pages of this type"),
        )

class IPageForm(Interface):
    """Marker interface for forms to be wrapped in a Deco interface.
    
    A special form layout template is defined for this marker interface, which
    references the site layout and invokes Block editing.
    """

class IOmittedField(Interface):
    """Marker interface for schema fields not to be shown in the Deco
    editor
    """

class ILayoutField(Interface):
    """Marker interface for the layout field
    """
