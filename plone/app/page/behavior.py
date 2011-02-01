from zope.interface import implements, alsoProvides
from zope import schema

from plone.directives import form

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
    form.fieldset('layout', label=_(u"Layout"), fields=['content'])

    content = schema.Text(
            title=_(u"Content"),
            description=_(u"Content of the object"),
            required=False,
        )
    
    sectionLayout = schema.ASCIILine(
            title=_(u"Section layout"),
            description=_(u"Default layout for pages in this section"),
            required=False,
        )
    
alsoProvides(ILayout, form.IFormFieldProvider)
alsoProvides(ILayout['content'], IOmittedField)

@form.default_value(field=ILayout['content'])
def getDefaultPageContent(data):
    
    # Avoid circular import
    from plone.app.page.utils import getDefaultPageLayout
    from plone.app.page.utils import resolveResource
    
    # Try to figure out the portal type from the view name. For add forms,
    # we get this from the add view itself
    
    obj = data.view
    portal_type = None
    while obj is not None:
        portal_type = getattr(obj, 'portal_type', None)
        if portal_type is not None:
            break
        obj = getattr(obj, '__parent__', None)
    
    if portal_type is None:
        return u""
    
    template = getDefaultPageLayout(portal_type)
    
    if template is None:
        return u""
    
    templatePath = data.context.absolute_url_path() + template
    return resolveResource(templatePath)
