+++
Description = "Fixing problems that even wildcard.fixpersistentutilities"
date = "2017-09-06T18:30:18+01:00"
title = "Identifying and fixing broken objects in a Plone website"
Tags = ["Plone","programming","cookbook", "tutorial"]

+++

I've removed ``plone.app.stagingbehavior`` from a website because the new ``plone.app.iterate`` has the same functionality. 
In addition, the p.a.s package was overriding adapters that I wanted to write.

Now, my problem was that I could no longer save any related items, I would get an error:

```
Module ZPublisher.Publish, line 138, in publish
Module ZPublisher.mapply, line 77, in mapply
Module ZPublisher.Publish, line 48, in call_object
Module plone.z3cform.layout, line 66, in __call__
Module plone.z3cform.layout, line 50, in update
Module plone.dexterity.browser.edit, line 64, in update
Module plone.z3cform.fieldsets.extensible, line 59, in update
Module plone.z3cform.patch, line 30, in GroupForm_update
Module z3c.form.group, line 145, in update
Module plone.app.z3cform.csrf, line 21, in execute
Module z3c.form.action, line 98, in execute
Module z3c.form.button, line 315, in __call__
Module z3c.form.button, line 170, in __call__
Module plone.dexterity.browser.edit, line 28, in handleApply
Module z3c.form.group, line 126, in applyChanges
Module zope.event, line 31, in notify
Module zope.component.event, line 24, in dispatch
Module zope.component._api, line 136, in subscribers
Module zope.component.registry, line 321, in subscribers
Module zope.interface.adapter, line 585, in subscribers
Module zope.component.event, line 32, in objectEventNotify
Module zope.component._api, line 136, in subscribers
Module zope.component.registry, line 321, in subscribers
Module zope.interface.adapter, line 585, in subscribers
Module plone.app.versioningbehavior.subscribers, line 62, in create_version_on_save
Module Products.CMFEditions.CopyModifyMergeRepositoryTool, line 301, in save
Module transaction._manager, line 101, in savepoint
Module transaction._transaction, line 260, in savepoint
Module transaction._transaction, line 257, in savepoint
Module transaction._transaction, line 690, in __init__
Module ZODB.Connection, line 1123, in savepoint
Module ZODB.Connection, line 623, in _commit
Module ZODB.Connection, line 658, in _store_objects
Module ZODB.serialize, line 422, in serialize
Module ZODB.serialize, line 431, in _dump
PicklingError: Can't pickle <class 'plone.app.stagingbehavior.interfaces.IStagingSupport'>: import of module plone.app.stagingbehavior.interfaces failed
```

The problems was that I had some broken relations in the zc.relation catalog. I've used a ZEO client debugging session:

```
# bin/zeoclient debug
...
>>> site = app['Plone']
>>> from zope.component import getUtility
>>> from zc.relation.interfaces import ICatalog
>>> catalog = getUtility(ICatalog, context=site)
>>> from zope.component.hooks import setSite
>>> setSite(site)
>>> list(catalog.findRelations())
[<persistent broken plone.app.stagingbehavior.relation.StagingRelationValue inst
ance '\x00\x00\x00\x00\x00\x06T\x12'>, <persistent broken plone.app.stagingbehav
ior.relation.StagingRelationValue instance '\x00\x00\x00\x00\x00\x14\x02\x12'>,
<persistent broken plone.app.stagingbehavior.relation.StagingRelationValue insta
nce '\x00\x00\x00\x00\x00\x14\x02\xd2'>]
```

In my case, I've just done:

```
>>> catalog.clear()
>>> import transaction; transaction.commit()
```

just to simplify the solution. But if other relations exist, ``clear()`` can't be used and instead the relationship values 
would need to be removed "manually"
