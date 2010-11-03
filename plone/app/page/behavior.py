import os.path

from zope.interface import implements, alsoProvides
from zope import schema

from plone.directives import form

from plone.app.page.interfaces import IOmittedField
from plone.app.page.interfaces import ILayoutField

from plone.app.page import PloneMessageFactory as _

DEFAULT_LAYOUT = open(
        os.path.join(
                os.path.dirname(__file__),
                'templates',
                'default-content-layout.html'
            )
    ).read().decode('utf-8')

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
            # XXX: This should be done by Deco; the default here should be empty,
            # since the default layout depends on Deco and plone.app.standardtiles
            default=DEFAULT_LAYOUT,
        )
    
alsoProvides(ILayout, form.IFormFieldProvider)
alsoProvides(ILayout['content'], IOmittedField)
