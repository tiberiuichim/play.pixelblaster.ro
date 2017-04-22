+++
date = "2017-01-25T23:09:45+01:00"
title = "Generate the route url for a Cornice service or resource"
tags = ["cookbook","Pyramid", "Cornice"]

+++

As far as I can tell, there's no documentation on how to generate the reverse
url for a [Cornice](https://github.com/Cornices/cornice) resource or service.
Suppose I want to publish a list of children resources and i want to make them
behave as linked data. For that, I want to be able to generate proper URLs,
based on the request URL.

This is some sample code to show how to achieve that, based on a side project
I'm working on:

```python
@resource(collection_path="/",
          path="/{id}", cors_origins=('*',), cors_max_age=3600)
class MLModelResource(object):

    def __init__(self, request):
        self.request = request

    def _model_url(self, ml):
        return self.request.route_url(self.__class__.__name__.lower(),
                                      id=ml.name)

    def serialize_model(self, ml, sess):
        res = {}
        res['name'] = ml.name
        res['labels'] = get_model_labels(ml, sess)
        res['can_predict'] = ml.can_predict()
        res['url'] = self._model_url(ml)
        return res

    def collection_get(self):
        sess = self.request.dbsession
        res = []
        for ml in sess.query(MLModel):
            res.append(self.serialize_model(ml, sess))
        return {'models': res}

```
Notice this line: `return self.request.route_url(self.__class__.__name__.lower(), id=ml.name)`
Cornice registers, for each resource, two routes: one named `collection_<classname>.lower()`
and another one with just the lower class name, `<classname>.lower()`.

For the regular services, Cornice register routes with the proper service name.
So, for a service such as:

```python
sampleserv = Service(name="sampleserv",
                  description="Use the sampleserv service",
                  path="/{name}/sampleserv",
                  cors_origins=('*',),
                  cors_max_age=3600)
```

the way to generate the route is:

```python
self.request.route_url('sampleserv', name='something')
```
