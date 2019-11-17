+++
Categories = ["Plone", "Volto", "Razzle"]
Description = ""
Tags = ["Plone", "Volto", "Razzle", "webpack", "cookbook"]
date = "2019-11-17T13:58:36+01:00"
menu = "main"
title = "Speedup volto razzle builds"

+++

I've been looking for a way to speedup Volto razzle/webpack builds, both while
developing and for "production" mode, when building the final bundle.
Fortunately, this solution exists and it's extremely easy to integrate.

Let's define the problem, to see how to approach it: what is Volto actually?
What do you get when you open, in your browser, a Volto frontend Plone website?
To greatly simplify (and I hope I didn't get anything wrong as I am not a Volto
core developer):

- the browser gets an HTML page which loads the CSS and JS bundles. This HTML
  is not an empty placeholder for the website, it comes pretty close to the
  actual final end result DOM.
- that HTML is created on the Volto server, which is based on the
  almost-standard Express nodejs HTTP server. It runs the same React code that
  would run in the browser, this process being the Server Side Rendering
- In order to have a streamlined development process, Volto uses a library
  called Razzle. This is useful in providing synchronized Hot Module Reloading
  (HMR), in both server and client processes.  Razzle is a layer of
  configuration on top of webpack.
- Webpack is a mega-framework that focuses on bundling static web resources.
  The CSS and JS files that it produces are dumped in the `build` folder and
  served by the Express server. Webpack is the one that reads the Javascript
  and JSX files, reads their import/require module declarations, discovers the
  coresponding files and puts them together in a .js file that can be served
  and read by the browsers. Webpack transforms the various files through
  its configured "loaders". For example, JSX files are loaded through the
  `babel-loader`, less files using a less loader, etc. See Volto's
  `razzle.config.js` file for details.
- Babel is a plugin-enabled compiler that takes files (like JSX or ES6+) and
  transforms (transpiles) them to "classic Javascript" code.

So, if my problem is that of slow compilation (generation of bundles by
Webpack), the solution must certainly be in Webpack's terrain. In the world of
compiled languages, compilation speedup is achieved by bundling compiled code
as libraries, which can then be linked to. DLL files in Windows, .so files in
Linux. Webpack has an official DLL-like plugin, but its not very easy to
integrate.

But there is another webpack plugin, mzgoddard/hard-source-webpack-plugin,
which can automatically cache big chunks of modules. In my tests, production
mode builds run 2 times faster (from 160 seconds to around 70 seconds), while
"cold starting" the razzle process (with `npm run start`) worked 10 times
faster: from 23 seconds to just 2 seconds.

To integrate it run:

```
npm install --save-dev hard-source-webpack-plugin
```

Then change your frontend's razzle.config.js to something like:

```
const HardSourceWebpackPlugin = require('hard-source-webpack-plugin');
const jsConfig = require('./jsconfig').compilerOptions;

const pathsConfig = jsConfig.paths;
let voltoPath = './node_modules/@plone/volto';
Object.keys(pathsConfig).forEach(pkg => {
  if (pkg === '@plone/volto') {
    voltoPath = `./${jsConfig.baseUrl}/${pathsConfig[pkg][0]}`;
  }
});

let config = require(`${voltoPath}/razzle.config`);
const razzleModify = config.modify;

module.exports = {
  modify: (config, { target, dev }, webpack) => {
    const vc = razzleModify(config, { target, dev }, webpack);
    const hardSource = new HardSourceWebpackPlugin();
    vc.plugins.push(hardSource);
    return vc;
  },
};
```
