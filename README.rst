.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

================================
collective.behavior.lastmodifier
================================

Adds a behavior that tracks down the last user that modified an object.

The ``plone.last_modifier`` behavior that can be added to any dexterity content.

Objects with that behavior will update the ``last_modifier`` attribute of the object
with the currently authenticated user id:

- when an object is created
- every time an ``ObjectModifiedEvent`` is fired.

Installation
------------

Install collective.behavior.lastmodifier by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.behavior.lastmodifier


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.behavior.lastmodifier/issues
- Source Code: https://github.com/collective/collective.behavior.lastmodifier


License
-------

The project is licensed under the GPLv2.
