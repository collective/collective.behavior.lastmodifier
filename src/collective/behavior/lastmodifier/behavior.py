# -*- coding: utf-8 -*-
from collective.behavior.lastmodifier import _
from plone import api
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.component import adapter
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent


class ILastModifier(model.Schema):

    last_modifier = schema.TextLine(
        title=_(u"Last modifier"),
        description=u"",
        required=False,
    )
    directives.omitted(IAddForm, "last_modifier")
    directives.omitted(IEditForm, "last_modifier")


alsoProvides(ILastModifier, IFormFieldProvider)


@implementer(ILastModifier)
@adapter(IDexterityContent)
class LastModifier(object):
    def __init__(self, context):
        self.context = context


def _set_last_modifier(obj):
    """For the moment expect that we can always find a user.
    In future versions maybe we will handle anonymous users.
    """
    ILastModifier(obj).last_modifier = api.user.get_current().getUserId()


@adapter(ILastModifier, IObjectAddedEvent)
def on_added(obj, event):
    _set_last_modifier(obj)


@adapter(ILastModifier, IObjectModifiedEvent)
def on_modified(obj, event):
    _set_last_modifier(obj)
