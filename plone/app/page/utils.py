from zope.component import queryUtility

from plone.subrequest import subrequest

from plone.dexterity.interfaces import IDexterityFTI

from plone.app.page.behavior import ILayout
from plone.app.page.interfaces import IPageFTI

from Acquisition import aq_inner
from Acquisition import aq_parent

_marker = object()

def getDefaultPageLayout(portal_type):
    fti = queryUtility(IDexterityFTI, name=portal_type)
    if fti is None or not IPageFTI.providedBy(fti):
        return None
    
    return fti.default_page_layout_template

def getDefaultSiteLayout(context):
    """Get the site layout to use by default for the given content object
    """
    
    # Note: the sectionLayout on context is for pages *under* context, not
    # necessarily context itself

    parent = aq_parent(aq_inner(context))
    while parent is not None:
        layout = ILayout(parent, None)
        if layout is not None:
            if layout.sectionLayout:
                return layout.sectionLayout
        parent = aq_parent(aq_inner(context))
    
    fti = queryUtility(IPageFTI, name=context.portal_type)
    if fti is None:
        return None
    
    return fti.default_site_layout

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
    
    for prop in oldFTI._properties:
        propId = prop['id']
        oldValue = getattr(oldFTI, propId, _marker)
        if oldValue is not _marker:
            kwargs[propId] = oldValue
    
    kwargs['title'] = title
    kwargs['description'] = description
    
    newFTI.manage_changeProperties(**kwargs)
    portal_types._setObject(newFTI.id, newFTI)

def changePageType(context, new_type, reindex=True):
    """Change the portal type (cateogry) of a page object
    """
    
    context.portal_type = new_type
    
    if reindex:
        context.reindexObject()

def extractCharset(response, default='utf-8'):
    """Get the charset of the given response
    """

    charset = default
    if 'content-type' in response.headers:
        for item in response.headers['content-type'].split(';'):
            if item.strip().startswith('charset'):
                charset = item.split('=')[1].strip()
                break
    return charset

def resolveResource(url):
    """Resolve the given URL to a unicode string
    """

    response = subrequest(url)
    resolved = response.getBody()
    
    if isinstance(resolved, str):
        charset = extractCharset(response)
        resolved = resolved.decode(charset)
    
    return resolved
