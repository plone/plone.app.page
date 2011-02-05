from zope.interface import implements

from plone.dexterity.fti import DexterityFTI

from plone.app.content.interfaces import INameFromTitle
from plone.app.dexterity.behaviors.metadata import IDublinCore

from plone.app.page.interfaces import IPageFTI
from plone.app.page.content import IPage
from plone.app.page.behavior import ILayout

from Products.CMFCore.browser.typeinfo import FactoryTypeInformationAddView

class PageFTI(DexterityFTI):
    """Factory type information for the Page type.
    
    There are some important policies encoded here:
    
        - The add view is always string:${folder_url}/++add++page, which
          means we use the standard (simplified) Page add form, even for
          clones of this FTI (different categories)
        - The immediate view is ``edit`` - this is where we go immediately
          after creation.
        - Behaviours default to a standard Plone set. Removing IDublinCore
          or ILayout is likely to be problematic.
        - We keep track of the default site layout for instances of this type
        - We keep track of the default page layout template for instances of
          this type
    
    """
    
    implements(IPageFTI)
    meta_type = "Page FTI"
    
    _properties = DexterityFTI._properties + (
            { 'id': 'default_site_layout', 
              'type': 'string',
              'mode': 'w',
              'label': IPageFTI['default_site_layout'].title,
              'description': IPageFTI['default_site_layout'].description,
            },
            { 'id': 'default_page_layout_template', 
              'type': 'string',
              'mode': 'w',
              'label': IPageFTI['default_page_layout_template'].title,
              'description': IPageFTI['default_page_layout_template'].description,
            },
        )
    
    immediate_view = 'edit'
    klass = 'plone.dexterity.content.Container'
    schema = IPage.__identifier__
    behaviors = [INameFromTitle.__identifier__, IDublinCore.__identifier__, ILayout.__identifier__]
    add_view_expr = "string:${folder_url}/++add++page"
    
    model_source = ""
    
    default_site_layout = "/++sitelayout++default/site.html"
    default_page_layout_template = "/++pagelayout++default/page.html"
    
    def __init__(self, *args, **kwargs):
        super(PageFTI, self).__init__(*args, **kwargs)
        self._setPropValue('add_view_expr', self.add_view_expr)

class FTIAddView(FactoryTypeInformationAddView):
    """Add view for the Page FTI type
    """

    klass = PageFTI
    description = u'Factory Type Information for pages'
