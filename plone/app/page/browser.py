from zope.interface import Interface, implements
from zope.component import adapts
from zope.publisher.browser import BrowserView

from zope import schema

from plone.dexterity.browser import add

from plone.app.blocks.layoutbehavior import ILayoutAware

from plone.app.page.interfaces import IPage

from plone.app.page import PloneMessageFactory as _

class IAddForm(Interface):
    """Form schema for minimalist add form
    """
    
    title = schema.TextLine(
            title=_(u"Title"),
        )
    
    description = schema.Text(
            title=_(u"Description"),
            required=False,
        )

class AddFormEditable(object):
    """Form adapter to make IAddForm work
    """
    
    implements(IAddForm)
    adapts(IPage)
    
    def __init__(self, context):
        self.context = context
    
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

class PageAddForm(add.DefaultAddForm):
    """Page add form
    """
    
    schema = IAddForm
    additionalSchemata = ()

class PageAddView(add.DefaultAddView):
    """Page add view for use in the ++add++ traversal adapter, which uses the
    add form above
    """
    form = PageAddForm

class View(BrowserView):
    """Default view for a page
    """

    def __call__(self):
        """Render the contents of the "content" field coming from
        the ILayoutAware behavior.

        This result is supposed to be transformed by plone.app.blocks.
        """
        return ILayoutAware(self.context).content