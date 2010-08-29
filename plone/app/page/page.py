"""This file contains a page type using Deco and Blocks
"""

from five import grok
from zope import schema
from zope.interface import Interface, implements

from plone.directives import form, dexterity
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from plone.app.layoutbehavior import ILayout


class IPage(form.Schema):

    # The default fieldset

    date = schema.Datetime(
            title=u"Date",
            required=False,
        )

    agenda = schema.Text(
            title=u"Agenda",
            required=False,
        )
    form.widget(agenda=WysiwygFieldWidget)

    recurrence = schema.Choice(
            title = u"Recurrence",
            values=('Yearly', 'Monthly', 'Weekly', 'Daily', 'Does not recur'),
            required=False,
        )


class View(grok.View):
    grok.context(IPage)
    grok.require('zope2.View')

    def render(self):
        """
        Render the contents of the "content" field coming from
        the plone.app.layoutbehavior behavior.
        This result is supposed to be transformed by plone.app.blocks.
        """
        return ILayout(self.context).content


class IFormDecoLayout(Interface):
    """Marker interface for forms to be wrapped in a Deco interface."""


class EditForm(dexterity.EditForm):
    implements(IFormDecoLayout)
    grok.context(IPage)


class AddForm(dexterity.AddForm):
    implements(IFormDecoLayout)
    grok.name('plone.app.page')
