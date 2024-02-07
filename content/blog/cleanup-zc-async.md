+++
Description = ""
tags = ["cookbook", "Plone"]
date = "2024-01-29T13:11:53Z"
title = "Cleanup zc async"
author = "Tiberiu Ichim"

+++

For my own reference, as I had to do a cleanup of zc.async tasks. The interface was too slow.

```
bin/zeo_client debug
queue = app._p_jar.root()['zc.async']['']
for i in range(len(queue)):
    queue.pull(0)
```
