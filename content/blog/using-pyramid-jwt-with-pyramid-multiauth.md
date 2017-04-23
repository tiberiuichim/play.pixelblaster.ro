+++
date = "2017-02-25T03:45:44+01:00"
title = "Using pyramid_jwt with pyramid_multiauth"
Tags = ["Pyramid","cookbook"]
Description = ""

+++

``pyramid_jwt`` has its own convenience method of registering as an
authentication policy, through ``config.set_jwt_authentication_policy``. It
does so because the constructor of its policy takes a lot of arguments, so it's
best to trust the package to do its own setup.

But this makes it a bit harder to use with ``pyramid_multiauth``, as you can't
easily pass the ``JWTAuthenticationPolicy`` policy to the
``multiauth.policies`` setting. Turns out that is not hard at all.
``pyramid_multiauth`` has its own magic trick of pulling the rabbit out of the
hat by reviving policies set with ``config.set_authentication_policy``, so, to
register the ``pyramid_jwt`` authentication policy, a simple module is needed:

```python
# this is module mystuff.auth

from pyramid_jwt import set_jwt_authentication_policy

def includeme(config):
    set_jwt_authentication_policy(config)

```

Now, in the settings ini file, register the policy as a module:

```ini
[my:app]
multiauth.policies = mystuff.auth
```

The trick that multiauth does is to register an action for the commit phase of
the configuration process that extracts the authentication set in place by the
module and adds it to a ``_policies`` list that is passed in the constructor
and stored by ``MultiAuthenticationPolicy``. A bit dirty, but brilliant.
