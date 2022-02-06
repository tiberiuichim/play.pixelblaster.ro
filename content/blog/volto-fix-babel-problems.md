+++
Categories = ["Volto", "Plone"]
Description = ""
Tags = ["cookbook","Plone", "Volto"]
date = "2022-02-06T18:05:18+02:00"
menu = "main"
title = "Custom Volto configuration to fix Babel problems with react-leaflet"

+++

I've started working on a new Leaflet-powered Volto map block and the first
thing that happened while loading react-leaftlet was an error reported by the
browser:

```
Module parse failed: Unexpected token (10:41) in @react-leaflet/core/esm/path.js
...
const options = props.pathOptions ?? {};
...
```

The problem is that is, for some reasons, the transpiled JS bundle includes
code using the [nulish coalescing operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Nullish_coalescing_operator)

This is already a [problem reported in
react-leaflet](https://github.com/PaulLeCam/react-leaflet/issues/877) and it
happens because the distributed transpiled library includes that code. Now, it
could be fixed by doing a safer transpilation in their build process, but
I don't care. This is a problem that can be taken care easily, in Volto.

Volto's Webpack (and, by extension, BabelJS) behavior can be customized through
the `razzle.config.js` file. My solution to fix the problem is this custom
razzle.config.js file included in my project:

```
const path = require('path');
const makeLoaderFinder = require('razzle-dev-utils/makeLoaderFinder');

const babelLoaderFinder = makeLoaderFinder('babel-loader');

const jsConfig = require('./jsconfig').compilerOptions;

const pathsConfig = jsConfig.paths;
let voltoPath = './node_modules/@plone/volto';
Object.keys(pathsConfig).forEach((pkg) => {
  if (pkg === '@plone/volto') {
    voltoPath = `./${jsConfig.baseUrl}/${pathsConfig[pkg][0]}`;
  }
});

const { modifyWebpackConfig, plugins } = require(`${voltoPath}/razzle.config`);

const customModifyWebpackConfig = ({ env, webpackConfig, webpackObject }) => {
  const config = modifyWebpackConfig({
    env,
    webpackConfig,
    webpackObject,
  });
  const babelLoader = config.module.rules.find(babelLoaderFinder);
  const { include } = babelLoader;
  const corePath = path.join(
    path.dirname(require.resolve('@react-leaflet/core')),
    '..',
  );
  const esmPath = path.join(
    path.dirname(require.resolve('react-leaflet')),
    '..',
  );

  include.push(corePath);
  include.push(esmPath);
  return config;
};

module.exports = { modifyWebpackConfig: customModifyWebpackConfig, plugins };
```

The solution envolves pushing the `@react-leaflet` package paths to Babel's
webpack loader's `include` option, so that they are included in the
transpilation process. By default all packages in `node_modules` are excluded
from the transpilation.

Incidentally, I'm aware of the
[volto-leaflet-block](https://github.com/adeweb-be/volto-leaflet-block/) addon,
and that one uses an older version of react-leaflet. Is this done because the
later version, `^4.0` has the tranpilation problem. In any case, all Volto
addons have the ability to "fix" webpack and babel issues similarly, via
`razzle.extend.js` placed in the addon package.
