+++
Tags = ["Flask","Pyramid","cookbook","python"]
Description = ""
date = "2017-08-14"
title = "Running Pyramid with Flask, in the same Python process"

+++

Thanks to the wonders of WSGI and well behaved frameworks, it is now trivial to mix and match applications and have them run in the same Python process. 

Normally, in a production scenario, uwsgi would be used to split and map the 
URL spaces to different apps, but for development it is simpler to just use good old PythonPaste. In my case, I've wanted
to have the RQ Dashboard (which is based on Flask) integrated with a Pyramid app that I'm working on. The following is needed:

* One entry point pointing to a Flask wsgi app. In my case, where the eea.corpus is the main package, I have:

```
    entry_points={
        'paste.app_factory': [
            'main = eea.corpus:main',
            'rq-dashboard = eea.corpus.async:dashboard',
    ],
```

The dashboard entry point is a typical Flask app, with some specifics about the RQ server:

```
def dashboard(global_config, **settings):
    """ WSGI entry point for the Flask app RQ Dashboard
    """

    redis_uri = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    p = parse.urlparse(redis_uri)
    host, port = p.netloc.split(':')
    db = len(p.path) > 1 and p.path[1:] or '0'

    redis_settings = {
        'REDIS_URL': redis_uri,
        'REDIS_DB': db,
        'REDIS_HOST': host,
        'REDIS_PORT': port,
    }

    app = Flask(__name__,
                static_url_path="/static",
                static_folder=resource_filename("rq_dashboard", "static")
                )
    app.config.from_object(rq_dashboard.default_settings)
    app.config.update(redis_settings)
    app.register_blueprint(rq_dashboard.blueprint)
    return app.wsgi_app
```

Now I can configure the production.ini with a composite app instead of its default:

```
[composite:main]
use = egg:Paste#urlmap
/ = corpus
/rq = rq-dashboard

[app:rq-dashboard]
use = egg:eea.corpus#rq-dashboard

[app:corpus]
use = egg:eea.corpus
pyramid.reload_templates = false
...
```
