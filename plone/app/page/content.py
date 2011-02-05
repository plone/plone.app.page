"""This file contains a page type using Deco and Blocks
"""

from five import grok
from zope.interface import implements

from plone.directives import form, dexterity
from zope import schema

from zope.lifecycleevent.interfaces import IObjectAddedEvent

from plone.app.page.interfaces import IPageForm
from plone.app.page.behavior import ILayout

from plone.app.page.utils import getDefaultPageLayout
from plone.app.page.utils import resolveResource

from plone.app.page import PloneMessageFactory as _

class IPage(form.Schema):
    """Page schema"""

class EditForm(dexterity.EditForm):
    implements(IPageForm)
    grok.context(IPage)

class IAddForm(form.Schema):
    """Form schema for minimalist add form
    """
    
    title = schema.TextLine(
            title=_(u"Title"),
        )
    
    description = schema.Text(
            title=_(u"Description"),
            required=False,
        )

class AddFormEditable(grok.Adapter):
    """Form adapter to make IAddForm work
    """
    
    grok.context(IPage)
    grok.provides(IAddForm)
    
    @property
    def title(self):
        return getattr(self.context, 'title', u"")
    @title.setter
    def title(self, value):
        self.context.title = value
    
    @property
    def description(self):
        return getattr(self.context, 'description', u"")
    @description.setter
    def description(self, value):
        self.context.description = value

class AddForm(dexterity.AddForm):
    grok.name('page')
    
    schema = IAddForm
    additionalSchemata = ()

@grok.subscribe(IPage, IObjectAddedEvent)
def setDefaultLayoutForNewPage(obj, event):
    """When a new page is created, set its layout based on the default in
    the FTI
    """
    layoutAware = ILayout(obj, None)
    if layoutAware is None:
        return
    
    portal_type = obj.portal_type
    template = getDefaultPageLayout(portal_type)
    
    if template is None:
        raise ValueError("Cannot find layout template for %s" % portal_type)
    
    templatePath = obj.absolute_url_path() + template
    layoutAware.content = resolveResource(templatePath)

class View(grok.View):
    grok.context(IPage)
    grok.require('zope2.View')

    def render(self):
        """Render the contents of the "content" field coming from
        the ILayout behavior.

        This result is supposed to be transformed by plone.app.blocks.
        """
        return ILayout(self.context).content
