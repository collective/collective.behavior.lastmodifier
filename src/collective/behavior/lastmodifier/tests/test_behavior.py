# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.behavior.lastmodifier.testing import INTEGRATION_TESTING
from plone import api
from zope.container.contained import ObjectModifiedEvent
from zope.event import notify

import unittest


class TestBehavior(unittest.TestCase):
    """Test that collective.behavior.lastmodifier is properly installed."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]

    def _create_doc(self):
        return api.content.create(container=self.portal, title="Foo", type="Document")

    def test_behavior(self):
        # When added picks up the creator userid
        with api.env.adopt_user("admin"):
            obj = self._create_doc()
        self.assertEqual(obj.last_modifier, "admin")

        with api.env.adopt_user("admin"):
            api.user.create(
                email="editor@example.com", username="editor", roles=["Editor"]
            )

        # When modified picks up the editor userid
        with api.env.adopt_user("editor"):
            notify(ObjectModifiedEvent(obj))

        self.assertEqual(obj.last_modifier, "editor")

    def test_field_not_displayed_on_add(self):
        with api.env.adopt_user("admin"):
            view = self.portal.restrictedTraverse("++add++Document")()

        self.assertNotIn("last_modifier", view)

    def test_field_not_displayed_on_edit(self):

        with api.env.adopt_user("admin"):
            obj = self._create_doc()
            view = obj.restrictedTraverse("@@edit")()

        self.assertNotIn("last_modifier", view)

    def test_field_displayed_on_view(self):

        with api.env.adopt_user("admin"):
            obj = self._create_doc()
            view = obj.restrictedTraverse("@@view")()

        self.assertIn("last_modifier", view)
