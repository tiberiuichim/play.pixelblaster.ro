#!/home/tibi/tools/bin/python

from lxml import etree
from urlparse import urlsplit
import codecs
import os
import pendulum

IN = "export_blog.xml"
OUT = "content"

BLOGPOST = u"""+++
draft = false
date = "{effective}"
title = "{title}"
keywords = "{subject}"
created = "{created}"
modified = "{modified}"
permaLink = "{permaLink}"
author = "Tiberiu Ichim"
+++

{text}
"""


def df(s):
    try:
        d = pendulum.parse(s)
    except Exception:   # convert to a naive timestring
        d = " ".join(s.split(" ")[:2])
        d = pendulum.parse(d)

    return d.to_iso8601_string()


def hugo_doc(e):
    fields = {}
    for field in e.xpath('field'):
        fields[field.get('name')] = (field.text or '').strip()

    if fields['keywords']:
        fields['subject'] = ', '.join(eval(fields['keywords']))

    for fname in ['created', 'modified', 'effective']:
        fields[fname] = df(fields[fname])

    fields['title'] = fields['title'].replace('"', '')
    return BLOGPOST.format(**fields)


def write_hugo_post(base, path, hugodoc):
    # Given a path in form /blog/archive/2016/10/13/how-to-make-the-linked-\
    #   object-editable-in-droppable-collective-cover-tiles
    # it makes the parent folders and write a doc at that location

    path = path[1:]     # remove the first /

    # create an index contents.lr at each parent
    frags = path.split('/')
    parents, slug = frags[:-1], frags[-1]

    name = slug + '.html'
    basedir = os.path.join(base, *parents)
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    fpath = os.path.join(basedir, name)

    with codecs.open(fpath, 'w', 'utf-8') as f:
        print "Writing", fpath
        f.write(hugodoc)


def main():
    if not os.path.exists(OUT):
        os.makedirs(OUT)

    with open(IN) as f:
        xml = f.read()

    e = etree.fromstring(xml)
    for entry in e.xpath('//entry'):
        link = entry.xpath("field[@name='permaLink']")[0].text
        path = urlsplit(link)[2]

        write_hugo_post(OUT, path, hugo_doc(entry))


if __name__ == "__main__":
    main()
