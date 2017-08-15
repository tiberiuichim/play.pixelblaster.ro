+++
Description = ""
Tags = ["Docker","cookbook", "Rancher", "cron"]
date = "2017-08-15"
title = "My recipe for cronjobs with Docker"

+++

One of the bigger annoyances when it comes to bigger application stacks (such as the typical Plone/Zope) is 
dealing with cron jobs and, in general, async tasks. The problem is that of the number of "pieces": having to deal with cron,
in addition to the rest of the stack only increases the maintainance burden: it's easy to forget that the stack needs to have
cronjobs installed, etc. One way to avoid it is to include the cron jobs in the stack, with a buildout recipe. That's ok for 
classic, non-docker based deployments.

In case of a dockerized deployment, the tendency is to allocate a container just for cron and have it perform the tasks. But
there's a problem with the kind of tasks it can perform: being a separate container, it will no longer have, by default,
direct access to all the resources it had as a cron job. For example, I prefer to expose Plone task entry points as zoperunnner
scripts instead of views triggered by curl or wget. A view would have to be protected some way: either forbiden in the frontend
server or protected by authorization, which then complicates the cron task and the maintainance burden: dedicated user account, 
keep those credentials secret and aside with the rest of the configuration, etc.

That being said, I needed to make a Rancher based deployment on a Plone stack. One of the most basic cron tasks that need to 
be done is zeopack, packing the Data.fs. The zeopack script created by the plone.recipe.zeoserver, to be able to perform 
properly, needs to be run from the same container as the Zeo server. This implies that I create a new Docker image and add
the necessary crontab information. Too much, and this work potentially needs to be duplicated for other cron tasks, as well.

My solution and my lucky discovery is a "crontab container". It will restart containers based on crontab-like rules. This
means that each cron task can be exposed as a separate container in a Docker Compose stack, once the container is started
it will perform its task and exit, then it will be restarted by the crontab container, at the specified moment.

This is how the services look like in a docker-compose file:
```
  container-crontab:
   image: rancher/container-crontab:v0.2.0
   container_name: container-crontab
   labels:
     io.rancher.scheduler.global: "true"
     io.rancher.scheduler.affinity:host_label: hostname=stack1
   volumes:
     - /var/run/docker.sock:/var/run/docker.sock
     - /var/lib/rancher:/var/lib/rancher

 cron-zeopack:
   # run zeopack each day at 3am
   image: plone:4.3.10
   labels:
     io.rancher.container.start_once: "true"
     io.rancher.scheduler.affinity:host_label: "hostname=stack1"
     cron.schedule: "0 0 3 * * ?"
   entrypoint: sh -c "/bin/sed -i -e s/127.0.0.1/zeoserver/ /plone/instance/bin/zeopack && /plone/instance/bin/zeopack"
   volumes:
     - plone-data:/data
 ```
 
 Unfortunately the zeopack script needs to be changed in place as it doesn't take proper command line arguments.
