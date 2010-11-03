"""This file contains a page type using Deco and Blocks
"""

from five import grok
from zope.interface import implements

from plone.directives import form, dexterity

from plone.app.page.behavior import ILayout
from plone.app.page.interfaces import IPageForm

class IPage(form.Schema):
    """Page schema"""

class EditForm(dexterity.EditForm):
    implements(IPageForm)
    grok.context(IPage)

class AddForm(dexterity.AddForm):
    implements(IPageForm)
    grok.name('plone.app.page')

class View(grok.View):
    grok.context(IPage)
    grok.require('zope2.View')

    def render(self):
        """Render the contents of the "content" field coming from
        the ILayout behavior.

        This result is supposed to be transformed by plone.app.blocks.
        """
        return ILayout(self.context).content
