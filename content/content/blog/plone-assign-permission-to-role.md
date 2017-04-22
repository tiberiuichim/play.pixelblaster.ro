+++
date = "2017-02-22T14:19:02+01:00"
title = "Plone: assign permission to role"
Description = ""
Tags = ["Plone","cookbook"]

+++

I always forget, and a quick search through the eggs folder didn't yield
anything easy to find: how to I assign a permission to a role, in a context?

This is a bit of code:

```python
from Products.DCWorkflow.utils import modifyRolesForPermission
from AccessControl.PermissionMapping import getPermissionMapping

perm = 'Delete objects'
pm = set(getPermissionMapping(perm, context, st=tuple))
pm.add('Contributor')
pm.add('Owner')
modifyRolesForPermission(wc, perm, tuple(pm))
```

This is based on code found in DCWorkflow. I know, the proper code would be:

```python
from AccessControl.Permission import Permission
p = Permission(name, data, obj)
p.setRole(role_name, True)
```

But I don't like that API. What is data? I don't know. I can understand name,
of course, and obj as the context. But data???
