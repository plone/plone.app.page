from zope.component import getUtility
from zope.component import queryUtility

from plone.i18n.normalizer.interfaces import IIDNormalizer

from plone.resource.interfaces import IResourceDirectory
from plone.resource.utils import queryResourceDirectory

from plone.registry.interfaces import IRegistry

from plone.dexterity.interfaces import IDexterityFTI

from plone.app.blocks.interfaces import DEFAULT_SITE_LAYOUT_REGISTRY_KEY
from plone.app.blocks.layoutbehavior import ILayoutAware

from plone.app.page.interfaces import PAGE_LAYOUT_FILE_NAME
from plone.app.page.interfaces import PAGE_LAYOUT_RESOURCE_NAME
from plone.app.page.interfaces import IPageFTI

from Acquisition import aq_inner
from Acquisition import aq_parent

_marker = object()

def getDefaultPageLayout(portal_type):
    fti = queryUtility(IDexterityFTI, name=portal_type)
    if fti is None or not IPageFTI.providedBy(fti):
        return None
    
    return fti.default_page_layout_template

def getPageSiteLayout(context):
    """Get the path to the site layout for a page. This is generally only
    appropriate for the view of this page. For a generic template or view, use
    getDefaultSiteLayout(context) instead.
    """
    
    layoutAware = ILayoutAware(context, None)
    if layoutAware is not None:
        if getattr(layoutAware, 'pageSiteLayout', None):
            return layoutAware.pageSiteLayout
    
    # Note: the sectionSiteLayout on context is for pages *under* context, not
    # necessarily context itself

    parent = aq_parent(aq_inner(context))
    while parent is not None:
        layout = ILayoutAware(parent, None)
        if layout is not None:
            if getattr(layout, 'sectionSiteLayout', None):
                return layout.sectionSiteLayout
        parent = aq_parent(aq_inner(parent))
    
    fti = queryUtility(IDexterityFTI, name=context.portal_type)
    if fti is not None and IPageFTI.providedBy(fti):
        if fti.default_site_layout:
            return fti.default_site_layout
    
    registry = queryUtility(IRegistry)
    if registry is None:
        return None
    
    return registry.get(DEFAULT_SITE_LAYOUT_REGISTRY_KEY)

def getPageTypes(portal_types, container=None):
    """Return a list of Page FTIs from the portal_types tool.
    
    If ``container`` is given, only list types that are addable in the
    given container.
    """
    return [fti for fti in portal_types.listTypeInfo(container)
                if IPageFTI.providedBy(fti)]

def clonePageType(portal_types, name, newName, title, description, **kwargs):
    """Given a Page FTI, create a new Page FTI with the given name, title,
    description and, optionally, other properties set.
    """

    oldFTI = portal_types[name]
    newFTI = oldFTI.__class__(newName)
    
    # Properties
    for prop in oldFTI._properties:
        propId = prop['id']
        if propId not in kwargs:
            oldValue = getattr(oldFTI, propId, _marker)
            if oldValue is not _marker:
                kwargs[propId] = oldValue
    
    kwargs['title'] = title
    kwargs['description'] = description
    kwargs['add_view_expr'] = 'string:${folder_url}/++add++%s' % newName
    
    newFTI.manage_changeProperties(**kwargs)
    
    # Actions
    actions = []
    for oldAction in oldFTI.listActions():
        actions.add(oldAction.clone())
    newFTI._actions = tuple(actions)
    
    # Aliases
    newFTI._aliases = oldFTI._aliases.copy()
    
    portal_types._setObject(newFTI.id, newFTI)

def changePageType(context, new_type, reindex=True):
    """Change the portal type (cateogry) of a page object
    """
    
    context.portal_type = new_type
    
    if reindex:
        context.reindexObject()

def createTemplatePageLayout(title, description, content, filename=PAGE_LAYOUT_FILE_NAME):
    """Create a new template page layout of the 'pagelayout' resource type
    in the ZODB portal_resources storage.
    
    A unique name will be normalised from the title and returned.
    """
    
    resources = getUtility(IResourceDirectory, name='persistent')
        
    # Create a normalized, unique name
    name = basename = getUtility(IIDNormalizer).normalize(title)
    idx = 1
    while queryResourceDirectory(PAGE_LAYOUT_RESOURCE_NAME, name) is not None:
        name = "%s-%d" % (basename, idx,)
        idx += 1
    
    # Ensure we have the sitelayouts resource type directory
    if PAGE_LAYOUT_RESOURCE_NAME not in resources:
        resources.makeDirectory(PAGE_LAYOUT_RESOURCE_NAME)
    pagelayouts = resources[PAGE_LAYOUT_RESOURCE_NAME]
    
    # Create a directory for the resource
    pagelayouts.makeDirectory(name)
    pagelayout = pagelayouts[name]
    
    # Write the contents.
    if isinstance(content, unicode):
        content = content.encode('utf-8')
    if isinstance(title, unicode):
        title = title.encode('utf-8')
    if isinstance(description, unicode):
        description = description.encode('utf-8')
    
    pagelayout.writeFile(filename, content)
    
    # Write the manifest
    pagelayout.writeFile('manifest.cfg', """\
[%s]
title = %s
description = %s
file = %s
""" % (PAGE_LAYOUT_RESOURCE_NAME, title, description, filename))

    return name
