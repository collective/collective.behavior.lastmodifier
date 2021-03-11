# -*- coding: utf-8 -*-
from collective.behavior.lastmodifier import _
from contextlib import contextmanager
from plone import api
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.component import adapter
from zope.globalrequest import getRequest
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent


_missing_value = object()


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

    @property
    def last_modifier(self):
        return self.context.last_modifier

    @last_modifier.setter
    def last_modifier(self, value):
        self.context.last_modifier = value


@contextmanager
def tracking_disabled(request=_missing_value):
    """Context manager that temporarily disables tracking the last modifier

    This might be useful, e.g., during migrations
    """
    if request is _missing_value:
        request = getRequest()

    try:
        old_value = request["lastmodifier.tracking.disabled"]
    except (AttributeError, KeyError, ValueError):
        # Either key is not there or this is not a dict-like
        old_value = _missing_value

    try:
        try:
            request["lastmodifier.tracking.disabled"] = True
        except Exception:
            # Probably the object is not dict-like
            pass
        yield request
    finally:
        if old_value == _missing_value:
            try:
                getattr(request, "other", request).pop("lastmodifier.tracking.disabled")
            except Exception:
                # Either key is not there or this is not dict-like
                pass
        else:
            request["lastmodifier.tracking.disabled"] = old_value


def _is_tracking_disabled():
    """Check if tracking should be disabled, usually it should not"""
    try:
        return getRequest()["lastmodifier.tracking.disabled"]
    except Exception:
        pass
    return False


def _set_last_modifier(obj):
    """For the moment expect that we can always find a user.
    In future versions maybe we will handle anonymous users.
    """
    if _is_tracking_disabled():
        return
    ILastModifier(obj).last_modifier = api.user.get_current().getUserId()


@adapter(ILastModifier, IObjectAddedEvent)
def on_added(obj, event):
    _set_last_modifier(obj)


@adapter(ILastModifier, IObjectModifiedEvent)
def on_modified(obj, event):
    _set_last_modifier(obj)
