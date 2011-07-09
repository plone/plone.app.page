from zope.interface import Interface
from zope.component import getUtility
from zope import schema

from z3c.form import form, field, button

from plone.i18n.normalizer.interfaces import IIDNormalizer

from plone.app.blocks.layoutbehavior import ILayoutAware

from plone.app.page.interfaces import PAGE_LAYOUT_RESOURCE_NAME
from plone.app.page.interfaces import PAGE_LAYOUT_FILE_NAME

from plone.app.page import utils
from plone.app.page import PloneMessageFactory as _

from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

class ICreateNewPageTypeForm(Interface):
    """Create a new page type from the current page
    """
    
    title = schema.TextLine(
            title=_(u"Title"),
            description=_(u"Title of the new page type"),
        )
    
    description = schema.Text(
            title=_(u"Description"),
            description=_(u"A short description of the new page type"),
            required=False,
        )
    
    change = schema.Bool(
            title=_(u"Change the type of this page to the new page type"),
            default=True,
        )

class CreateNewPageTypeForm(form.Form):
    
    fields = field.Fields(ICreateNewPageTypeForm)
    ignoreContext = True
    
    label = _(u"Create new page type")
    description = _(u"You can save this page as a template under a new name, " +
                    u"making it possible to add new pages like this elsewhere " +
                    u"in the site")
    
    @button.buttonAndHandler(_(u"Save"))
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        
        title = data['title']
        description = data['description']
        change = data['change']
        
        layoutAware = ILayoutAware(self.context)
        
        content = layoutAware.content
        siteLayout = layoutAware.pageSiteLayout
        
        # Save the resource for the template page layout
        pagelayout = utils.createTemplatePageLayout(title, description, content)
        
        # Clone the page type
        
        portal_types = getToolByName(self.context, 'portal_types')
        
        name = basename = getUtility(IIDNormalizer).normalize(title)
        idx = 1
        while name in portal_types:
            name = "%s-%d" % (basename, idx,)
            idx += 1
        
        filename = PAGE_LAYOUT_FILE_NAME
        utils.clonePageType(portal_types, self.context.portal_type, name,
                title=title,
                description=description,
                default_site_layout=siteLayout,
                default_page_layout_template="/++%s++%s/%s" % (PAGE_LAYOUT_RESOURCE_NAME, pagelayout, filename,),
            )
        
        # Change the current item's page type if applicable
        if change:
            utils.changePageType(self.context, name)
        
        self.request.response.redirect(self.context.absolute_url())
    
    @button.buttonAndHandler(_(u'Cancel'))
    def cancel(self, action):
        self.request.response.redirect(self.context.absolute_url())

class ManageLayoutsForm(form.EditForm):
    
    fields = field.Fields(ILayoutAware).omit('content')
    
    label = _(u"Manage layouts")
    description = _(u"Choose the site layout to use for this page, and for " +
                    u"any pages underneath it in this section.")
    
    def getContent(self):
        return ILayoutAware(self.context)
    
    @button.buttonAndHandler(_(u"Save"))
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        
        self.applyChanges(data)
        IStatusMessage(self.request).add(_(u"Changes saved"), "info")
        self.request.response.redirect(self.context.absolute_url())
        
    @button.buttonAndHandler(_(u'Cancel'))
    def cancel(self, action):
        self.request.response.redirect(self.context.absolute_url())
