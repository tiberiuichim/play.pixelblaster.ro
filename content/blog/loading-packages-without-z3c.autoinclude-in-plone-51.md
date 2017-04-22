+++
Tags = ["Plone","cookbook"]
date = "2017-02-25T19:29:37+01:00"
title = "Loading packages without z3c.autoinclude in Plone 5.1"

+++

The new Plone 5.1 development buildout doesn't include a zcml property in its
[instance] section. It is no longer needed, with all eggs already providing
a z3c.autoinclude entrypoint. This, unless you want to load an older package
which doesn't have such an entry point. That's when the trouble starts. Adding
a, for example:

```ini
[instance]
...
zcml +=
    cs.auth.facebook
```

doesn't work. There is really no zcml property in any of the extended cfg file,
so Zope will try to load this package first, which will result in a "permission
not defined" zcml error. My fix is to include the Products.CMFPlone egg,
something like this:


```ini
[instance]
...
zcml =
    Products.CMFPlone
    cs.auth.facebook
```
