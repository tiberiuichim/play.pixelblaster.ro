+++
Categories = ["Python","cookbook"]
Description = ""
Tags = ["Python","cookbook"]
date = "2017-12-18T16:22:22+02:00"
title = "A quick and dirty mini-plugin system for Python"

+++

Inspired by Pyramid's and venusian's ``scan()`` call, I've reimplemented an
auto-discovery system for plugins. The problem is simple.

Suppose we want to "register" a series of functions that can run automatically,
based on aspects set in the calling environment. The simples and easiest
solution is something like:

```python
# in some module, as a global declaration:
from somethingA import runner_A
from somethingB import runner_B

runners = [
  runner_A,
  runner_B
]

# then, maybe in some function:

def main():
  # ...
  for runner in runners:
    runner()
```

This is dirty and ugly, but very straight forward. A more elegant, but more
complicated solution would be this very simple application of decorators:

```
runners_registry = []


def register(func):
    runners_registry.append(func)

    return func

```

This can be used to decorate a function and add a reference to that function
in the registry:

```python
@registry
def clean():
  pass
```

But now, to "activate" the registry call, one needs to make sure that the
module containing that function is imported at startup. Ugly.


I prefer a version that makes development easier, as it doesn't require
updating any code after a new "plugin module" is developed. It's inspired
by venusian's ``scan()`` call, but really bare bones and without any feature.
Just very straight forward "import all found modules to activate their
decorators"

```
def scan(namespace):
    """ Scans the namespace for modules and imports them, to activate decorator
    """

    import importlib
    import pkgutil

    name = importlib.util.resolve_name(namespace, package=__package__)
    spec = importlib.util.find_spec(name)

    if spec is not None:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for finder, name, ispkg in pkgutil.iter_modules(module.__path__):
            spec = finder.find_spec(name)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
```

Now I can use it like:


```python

def main():
  scan('somepackage.plugins')
```
