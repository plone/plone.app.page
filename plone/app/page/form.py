import os.path

from plone.z3cform.templates import ZopeTwoFormTemplateFactory
from plone.app.z3cform.interfaces import IPloneFormLayer

import plone.app.page
from plone.app.page.page import IFormDecoLayout

path = lambda p: os.path.join(os.path.dirname(plone.app.page.__file__), p)

# Override the plone layout wrapper with an special one to work with Deco
form_template_factory = ZopeTwoFormTemplateFactory(
    path('form.pt'),
    form=IFormDecoLayout,
    request=IPloneFormLayer)
