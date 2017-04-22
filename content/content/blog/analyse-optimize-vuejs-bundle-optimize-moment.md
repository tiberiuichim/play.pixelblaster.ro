+++
Tags = ["cookbook","webpack", "vuejs", "quasar-framework"]
date = "2017-03-02T14:54:52+01:00"
title = "Analyse and optimize a webpack vuejs bundle"
Description = ""

+++

At around 450 kb of javascript code, a Quasar distribution bundle seems a bit
too big. The following short recipe applies to an app generated from the
Quasar Framework default template, but it probably applies to any vuejs project
that uses vue-loader, and even any project using webpack.


First, we want to analyse what's inside the bundle. A good utility is
webpack-bundle-analyzer, but how to use it?

1. Configure the webpack to write the stats to a json file. In my case, I've
   changed the build/script.build.js to have something like this:

```javascript
var fs = require('fs')

webpack(webpackConfig, function (err, stats) {
  if (err) throw err

  // this writes the stats.json file with webpack statistics
  fs.writeFileSync('./stats.json', JSON.stringify(stats.toJson()));

  process.stdout.write(stats.toString({
...
```

So, only added two lines: the ``required('fs')`` and ``fs.writeFileSync``.

2. Install the webpack-bundle-analyzer with ``npm install --save-dev``.

3. Build the bundle: ``npm run build``

4. Analyze the bundle:

``node_modules/.bin/webpack-bundle-analyzer stats.json dist/ -p 4000``

This opens a new http server on port 4000, where the bundle contents can be
analysed. In my case, I found that moment.js adds about 70kb of gzipped content
that can be stripped during the webpack process. But how? With a webpack
IgnorePlugin.

In the build/webpack.base.conf, in the plugins listing, I've added a new
plugin:

```javascript

module.exports = {
  ...
  plugins: [
    new webpack.DefinePlugin({
      'process.env': config[env.prod ? 'build' : 'dev'].env,
      'DEV': env.dev,
      'PROD': env.prod,
      '__THEME': '"' + env.platform.theme + '"'
    }),
    new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/),
    new webpack.LoaderOptionsPlugin({
      minimize: env.prod,
...
```

Notice the IgnorePlugin line, inserted between the other two. With this in
place, I've reduced the JS vender bundle size to 340 KB, which further reduces
to 90 KB when gziped, a figure that I can be absolutely OK with.
