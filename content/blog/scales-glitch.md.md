+++
Description = "Scales were regenerating and I found why"
Tags = ["Plone"]
date = "2024-02-07T06:06:21Z"
title = "Image scales wrongly regenerating"

+++

I had a problem with my Frankenstein stack of Plone 4 with various bits (core
libraries) upgraded on it. Here's a description of my bug:

When I upload an image and try to use it in a Volto block that referenced its
image scales download url (such as `@@images/<random-uuid4>.jpg`) the image URL
didn't work, it resulted in 404 error. When I reindexed the image in the
catalog, then it worked. Now, the funky part is that I could reproduce the
problem not only on my "doomed" Plone 4 stack, but also in the modern Plone
6 stack that we use for our main customer.

I traced the problem to the fact that the context content was changing its
`_p_mtime` which caused its scales to be regenerated, due to [this check in
plone.scale](https://github.com/plone/plone.scale/blob/47c1102ed833b53d267a5bd0881b85eed0c6d93c/plone/scale/storage.py#L306)

I solved my particular problem by monkey-patching the `_modified_since`
function and setting its default offset keyword argument to be 3 seconds.
I think the latest `plone.scale` code has a more stable "algorithm" to generate
the scale uids, but the old code that I'm using always generates a random uuid4
uid, which aggravates the problem.

So, the main take-away is: if for some reason your code causes the `_p_mtime`
of your persistent objects to change during the same transaction, and you have
code that reads the scales information, those scales get regenerated. And if
the scale uids change, I don't think they're even being reindexed.
