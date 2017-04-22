+++
date = "2017-02-22T06:33:34+01:00"
title = "Python packaging vs npm"
Tags = ["Python","npm", "rant"]
draft = false
+++

I admit, Python packages are a bit more difficult to understand, for a newbie.
I have witnessed this problem a lot, lately, when dealing with new people
trying to learn the Python development process.

There is a mountain of information that needs to be climbed, to understand
Python packages:

* the namespace concept
* the matter of OS security
* the full cycle of an application, from development to deployment and
  maintainance

And this are just basics, in addition to the
distutils/setuptools/virtualenv/pip or zc.buildout information that needs to be
digested, to properly use python packages.

But the (unintended) consequence is that the existing published packages on
PyPI are usually high(er) quality, and some of them are even documented.
I don't think there's such a brag right in the Python community "I have
published X amount of packages on pypi".

Evil and stupid and a huge waste of time. How else would I qualify this
package, hello.js, installed by mistaked when I actually wanted hellojs:

```javascript
var sayHello = function  (argument) {
	// body...
	return "sayHello";
}

module.exports=sayHello;
```

Why in the world is this thing allowed to polute the world with its bits? I've
read about "placeholder packages" and "reserving names" and that's crazy.
Developers should focus on quality of code, not bragging rights.
