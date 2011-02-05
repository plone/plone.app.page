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
    form.fieldset('layout', label=_(u"Layout"), fields=['content', 'sectionLayout'])

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