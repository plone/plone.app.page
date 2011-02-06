from zope.interface import implements
from zope.component import getUtility

from zope.schema.interfaces import IVocabularyFactory

from plone.dexterity.fti import DexterityFTI

from plone.app.content.interfaces import INameFromTitle
from plone.app.dexterity.behaviors.metadata import IDublinCore

from plone.app.page.interfaces import IPageFTI
from plone.app.page.interfaces import PAGE_LAYOUT_RESOURCE_NAME
from plone.app.page.interfaces import PAGE_LAYOUT_FILE_NAME

from plone.app.page.content import IPage
from plone.app.page.layoutbehavior import ILayout

from Products.CMFCore.browser.typeinfo import FactoryTypeInformationAddView

class PageFTI(DexterityFTI):
    """Factory type information for the Page type.
    
    There are some important policies encoded here:
    
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
              'type': 'selection',
              'select_variable': 'availableSiteLayouts',
              'mode': 'w',
              'label': IPageFTI['default_site_layout'].title,
              'description': IPageFTI['default_site_layout'].description,
            },
            { 'id': 'default_page_layout_template', 
              'type': 'selection',
              'select_variable': 'availablePageLayouts',
              'mode': 'w',
              'label': IPageFTI['default_page_layout_template'].title,
              'description': IPageFTI['default_page_layout_template'].description,
            },
        )
    
    immediate_view = 'edit'
    klass = 'plone.dexterity.content.Container'
    schema = IPage.__identifier__
    behaviors = [INameFromTitle.__identifier__, IDublinCore.__identifier__, ILayout.__identifier__]
    
    model_source = ""
    
    default_site_layout = None # use global default
    default_page_layout_template = "/++%s++default/%s" % (PAGE_LAYOUT_RESOURCE_NAME, PAGE_LAYOUT_FILE_NAME,)
    
    def availableSiteLayouts(self):
        factory = getUtility(IVocabularyFactory, name=u"plone.app.page.availableSiteLayouts")
        vocabulary = factory(self)
        return [t.value for t in vocabulary]
        
    def availablePageLayouts(self):
        factory = getUtility(IVocabularyFactory, name=u"plone.app.page.availablePageLayouts")
        vocabulary = factory(self)
        return [t.value for t in vocabulary]

class FTIAddView(FactoryTypeInformationAddView):
    """Add view for the Page FTI type
    """

    klass = PageFTI
    description = u'Factory Type Information for pages'
