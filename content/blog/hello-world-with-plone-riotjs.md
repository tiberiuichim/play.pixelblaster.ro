+++
Description = ""
Tags = ["Plone","cookbook", "Javascript", "requirejs", "riotjs"]
date = "2017-04-23T16:12:13+03:00"
title = "Hello world with Plone and Riot (Javascript frontent library)"

+++

I'm working on a somewhat weird experiment. My end goal is to have a user
friendly (and mobile friendly) faceted search interface over the items of
a collection.

Seen through the eyes of my recent experience with VueJS, the
classic Plone frontend APIs, such as JQuery and Patternslib/Mockup seem
outdated and hard to digest. Any dedicated frontend UI library will seem much
friendlier.

My self-imposed requirements were:

* easy to work with, easily integrated. I don't want another full blown
  webpack, babel transpiled, full repo needing puzzle piece of software.
* nice, easy to learn API
* should have a router
* should be small. Plone already loads too much.
* should cooperate with the existing Plone Patternslib, which is mostly jQuery
  based
* older browsers compatibility is a plus

To all of the above, after a short look at MithrilJS, it seems like the best
match is Riot.  For the backend I've installed
(plone.restapi)[https://github.com/plone/plone.restapi] and this will grant
a JSON based access, from the Plone backend, to the frontend API library.

The first hurdle was figguring out how to load Riot in Plone. The ``Mismatched
anonymous define() module:`` error in the new ``:q`` puzzle of our time. Simply
trying to load the Riot library with a ``<script>`` tag is impossible due to
the, now available, AMD support with requirejs in Plone. After much
headscratching, reading some Plone related forum threads that made no sense,
I've finally figured it out. The main problem is that I foolishly thought that,
by registering a new resource, in the Resource Registries configlet, with the
proper URL, would be enough for Plone to understand that it's dealing with
a requirejs compatible library. Even "manually" declaring, in the resource
registration,  that it exports "riot" as a module didn't help.

The solution is to register a simple ``++resource++my/app.js`` file in the
Resource Registries, with the following contents:

```javascript
requirejs.config({
  paths: {
    'riot': ['//cdnjs.cloudflare.com/ajax/libs/riot/3.4.2/riot'],
    'tags': ['++resource++my/riot-tags']
  },
  shim: {
    'tags': ['riot']
  }
});

require(['riot', 'tags'], function(riot) {
  riot.mount('*');
  return {};
});
```

First, we register two libraries: 'riot' and 'tags'. Notice that, while they
all point to a js file, they're missing the .js extension. At last, there's
a simple function, integrated with the requirejs machinery, that triggers the
riotjs tag mounting process. But what is that ``riot-tags``, you'll ask?

Well, one thing I love about Vuejs (beyond its API simplicity) is the single-file
components. The Riot tags (basically the equivalent of components) are single
.tag files that can be compiled and automatically mounted in the full page DOM.
Neat.

Now, for that promised "hello world": in my statics folder, I've created a new
folder called "tags". Inside, the simplest component:

```html
<hello>
  <h2>HTML text</h2>

  <script>
    console.log('hello from script')
  </script>
</hello>
```

saved as "hello-world.tag".

Now, compile the whole tags folder as a single js file, using the riot compiler
(easily installed with ``npm -g install riot``):

```
$ riot -m -w ./tags/ riot-tags.js
```

Run in the statics folder, this will create the riot-tags.js file, which will
be further included as detailed above.

And finally, in a Plone template, insert a simple ``<hello></hello>`` tag.
