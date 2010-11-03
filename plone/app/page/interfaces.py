from zope.interface import Interface

class IPageForm(Interface):
    """Marker interface for forms to be wrapped in a Deco interface.
    """

class IOmittedField(Interface):
    """Marker interface for schema fields not to be shown in the Deco
    editor
    """

class ILayoutField(Interface):
    """Marker interface for the layout field
    """
