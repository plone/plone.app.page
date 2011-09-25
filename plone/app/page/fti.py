from zope.interface import implements
from zope.component import getUtility

from zope.schema.interfaces import IVocabularyFactory

from plone.dexterity.fti import DexterityFTI

from plone.app.content.interfaces import INameFromTitle

from plone.app.dexterity.behaviors.metadata import IDublinCore

from plone.app.blocks.layoutbehavior import ILayoutAware

from plone.app.page.interfaces import IPageFTI
from plone.app.page.interfaces import PAGE_LAYOUT_RESOURCE_NAME
from plone.app.page.interfaces import PAGE_LAYOUT_FILE_NAME

from Products.CMFCore.browser.typeinfo import FactoryTypeInformationAddView

class PageFTI(DexterityFTI):
    """Factory type information for the Page type.
    
    There are some important policies encoded here:
    
        - The immediate view is ``edit`` - this is where we go immediately
          after creation.
        - Behaviours default to a standard Plone set. Removing IDublinCore
          or ILayoutAware is likely to be problematic.
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
    klass = 'plone.app.page.content.Page'
    behaviors = [INameFromTitle.__identifier__, IDublinCore.__identifier__, ILayoutAware.__identifier__]
    
    model_source = """\
    <model xmlns="http://namespaces.plone.org/supermodel/schema">
        <schema>
        </schema>
    </model>
    """
    
    default_page_layout_template = "/++%s++default/%s" % (PAGE_LAYOUT_RESOURCE_NAME, PAGE_LAYOUT_FILE_NAME,)
    
    @property
    def default_site_layout(self):
        return self.__dict__.get('default_site_layout', None)
    @default_site_layout.setter
    def default_site_layout(self, value):
        if value == '(Default)':
            value = None
        self.__dict__['default_site_layout'] = value
    
    def availableSiteLayouts(self):
        factory = getUtility(IVocabularyFactory, name=u"plone.availableSiteLayouts")
        vocabulary = factory(self)
        return ['(Default)'] + [t.value for t in vocabulary]
        
    def availablePageLayouts(self):
        factory = getUtility(IVocabularyFactory, name=u"plone.availablePageLayouts")
        vocabulary = factory(self)
        return [t.value for t in vocabulary]

class FTIAddView(FactoryTypeInformationAddView):
    """Add view for the Page FTI type
    """

    klass = PageFTI
    description = u'Factory Type Information for pages'
