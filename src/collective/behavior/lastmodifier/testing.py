# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from Products.CMFCore.utils import getToolByName

import collective.behavior.lastmodifier


class CollectiveBehaviorLastmodifierLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.behavior.lastmodifier)

    def setUpPloneSite(self, portal):
        pt = getToolByName(portal, "portal_types")
        # Enable the behavior for pages
        fti = pt["Document"]
        fti.behaviors = fti.behaviors + ("plone.last_modifier",)


COLLECTIVE_BEHAVIOR_LASTMODIFIER_FIXTURE = CollectiveBehaviorLastmodifierLayer()


INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_BEHAVIOR_LASTMODIFIER_FIXTURE,),
    name="CollectiveBehaviorLastmodifierLayer:IntegrationTesting",
)
