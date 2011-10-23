# A Todo App (with Backbone.js, Require.js, Flask, and MongoDB)

This is an extension of the Todos app included in the Backbone.js repository,
by [Jérôme Gravel-Niquet](http://jgn.me/).

The App demonstrates how to integrate several technologies together beyond what is
done in the original, and gives an idea of how to put together a full stack app.

* Backbone.js - Client side framework.
* Require.js - Async resource loading.
* Flask - A simple python webapp to provide a REST interface.
* MongoDB - Persistance for the client app.

The markup for the client app has also been moved server side, and is fetched as needed
via jQuery.ajax.

The app runs with a single MongoDB node, but scripts are provided to show how a replicated
setup works as well.

Backlog:

* require.js optimizer
* client side automated tests with jasmine
* serving client side assets from CDN
