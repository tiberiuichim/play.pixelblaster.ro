+++
Tags = ["Plone","cookbook"]
Description = ""
date = "2017-02-23T16:53:16+01:00"
title = "Test for an interface provided by object in plone action condition"

+++

Quick tip: how to test if the context provides an interface, with an expression
set as the condition:

```
python:object.restrictedTraverse("@@plone_interface_info").provides('dotted.path.to.IMyFancyInterface')
```
