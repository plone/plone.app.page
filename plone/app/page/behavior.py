import urlparse

from zope.interface import implements, alsoProvides

from plone.directives import form
from zope import schema

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
    form.fieldset('layout', label=_(u"Layout"), fields=['content', 'pageSiteLayout', 'sectionLayout'])

    content = schema.Text(
            title=_(u"Content"),
            description=_(u"Content of the object"),
            required=False,
        )
    
    pageSiteLayout = schema.ASCIILine(
            title=_(u"Section layout"),
            description=_(u"Current site layout"),
            required=False,
        )
    
    sectionLayout = schema.ASCIILine(
            title=_(u"Section layout"),
            description=_(u"Default site layout for pages in this section"),
            required=False,
        )
    
    
    
alsoProvides(ILayout, form.IFormFieldProvider)
alsoProvides(ILayout['content'], IOmittedField)
alsoProvides(ILayout['pageSiteLayout'], IOmittedField)
alsoProvides(ILayout['sectionLayout'], IOmittedField)

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
    
    portal_type = obj.portal_type
    template = getDefaultPageLayout(portal_type)
    
    if template is None:
        raise ValueError("Cannot find layout template for %s" % portal_type)
    
    templatePath = urlparse.urljoin(obj.absolute_url_path(), template)
    layoutAware.content = resolveResource(templatePath)
