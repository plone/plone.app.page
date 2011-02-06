import urlparse

from zope.interface import implements, alsoProvides
from zope.component import adapter

from plone.directives import form
from zope import schema

from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from plone.app.page.interfaces import IOmittedField
from plone.app.page.interfaces import ILayoutField

from plone.app.page import PloneMessageFactory as _

class LayoutField(schema.Text):
    """A field used to store layout information
    """
    
    implements(ILayoutField)

class ILayout(form.Schema):
    """Behavior interface to make a type support layout.
    """
    form.fieldset('layout', label=_(u"Layout"), fields=['content', 'pageSiteLayout', 'sectionSiteLayout'])

    content = schema.Text(
            title=_(u"Content"),
            description=_(u"Content of the object"),
            required=False,
        )
    
    pageSiteLayout = schema.Choice(
            title=_(u"Section layout"),
            description=_(u"Current site layout"),
            vocabulary="plone.app.page.availableSiteLayouts",
            required=False,
        )
    
    sectionSiteLayout = schema.Choice(
            title=_(u"Section layout"),
            description=_(u"Default site layout for pages in this section"),
            vocabulary="plone.app.page.availableSiteLayouts",
            required=False,
        )
    
alsoProvides(ILayout, form.IFormFieldProvider)
alsoProvides(ILayout['content'], IOmittedField)
alsoProvides(ILayout['pageSiteLayout'], IOmittedField)
alsoProvides(ILayout['sectionSiteLayout'], IOmittedField)

@adapter(ILayout, IObjectModifiedEvent)
def setDefaultLayoutForNewPage(obj, event):
    """When a new page is created, set its layout based on the default in
    the FTI
    """
    
    # Avoid circular import
    from plone.app.page.utils import getDefaultPageLayout
    from plone.app.page.utils import resolveResource
    
    layoutAware = ILayout(obj, None)
    if layoutAware is None:
        return
    
    # Initialise object
    layoutAware.content = ILayout['layoutAware'].missing_value
    layoutAware.pageSiteLayout = ILayout['pageSiteLayout'].missing_value
    layoutAware.sectionSiteLayout = ILayout['sectionSiteLayout'].missing_value
    
    portal_type = obj.portal_type
    template = getDefaultPageLayout(portal_type)
    
    if template is None:
        raise ValueError("Cannot find layout template for %s" % portal_type)
    
    templatePath = urlparse.urljoin(obj.absolute_url_path(), template)
    layoutAware.content = resolveResource(templatePath)
