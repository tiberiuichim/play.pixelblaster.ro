+++
Categories = ["Plone","Volto"]
Description = ""
Tags = ["Plone","Volto"]
date = "2019-12-11T21:35:24+01:00"
title = "A Volto gotcha when dealing with async calls"

+++

Just some quick notes, in case this might help someone. After quite a bit of time and tests in trying to use ``asyncConnect`` to get data in a Volto component view (strictly focusing on the SSR side), I've realized that what I'm trying to do is not supported by the redux-connect library. 

In Volto, right now there are two components that use asyncConnect: App.jsx and Search.jsx. The purpose of asyncConnect is to have the server side rendered page "dynamic", depending on the input from the originating request. So, for example, a curl grab on https://volto.kitconcept.com/search?SearchableText=Plone will generate HTML that comes prefilled with the search results, instead of those results being loaded on the client, when they arrive. The use of asyncConnect calls in those two components makes the rendering of those components first wait for the backend data to arrive, then it will render them on the server and feed the populated HTML to the client.
 
So why couldn't I make use of asyncConnect in my components? There's a ticket on the react-redux Github page that better explains it: https://github.com/makeomatic/redux-connect/issues/45
In short, react-connect loads the async data on router load and is only aware of asyncConnected components if they are a component referenced directly by the router.

I think it's important for Volto to overcome this issue, as it imposes some limitations on what is possible in regular component views. For the moment, these are the options, if you need data that's not already provided by the App.jsx asyncConnect (which loads breadcrumbs, content, navigation, types and workflow):

- customize App.jsx or View.jsx (or any other component that's referenced in ``defaultRoutes``) and asyncConnect your own actions there
- override Plone's serializers to include the data you need, so that you can grab it from the ``state.content``
- move your view to a separate route, where you can use asyncConnect.
- customize routes.js and process the defaultRoutes so that you can point the ``/`` View route to your own asyncConnect wrapper over View.

For the future, here are some libraries that might provide a solution to this problem:

- An article by Mozilla explaining how to do a double rendering: http://farmdev.com/thoughts/107/why-server-side-rendering-in-react-is-so-hard/ 
- Vue's solution in dealing with this problem: https://github.com/vuejs/vue/pull/9017
- https://github.com/FormidableLabs/react-ssr-prepass
- https://github.com/overlookmotel/react-async-ssr
- https://github.com/ctrlplusb/react-async-component

As far as I understand, there's no drop-in solution, some sort of API needs to be developed on the Volto side, to provide a way for components to declare their SSR prefetch dependencies.

Many thanks to my colleague Mihai Macaneata who has patiently walked with me through understanding the source of this problems. Cheers!
