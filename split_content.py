#!/home/tibi/tools/bin/python

from lxml import etree
# from lxml import html
from urlparse import urlsplit
import codecs
import os

IN = "export_blog.xml"
OUT = "content"

TPL = u"""_model: blog-post
---
title: {title}
---
permaLink: {permaLink}
---
created: {created}
---
modified: {modified}
---
pub_date: {effective}
---
keywords: {subject}
---
body:
{text}
---
author: Tiberiu Ichim
"""


def lektorize(e):
    fields = {}
    for field in e.xpath('field'):
        fields[field.get('name')] = (field.text or '').strip()

    if fields['keywords']:
        fields['subject'] = ', '.join(eval(fields['keywords']))
    return TPL.format(**fields)


def write_lektor_document(base, path, content):
    # Given a path in form /blog/archive/2016/10/13/how-to-make-the-linked-\
    #   object-editable-in-droppable-collective-cover-tiles/manage_metadata
    # it writes a contents.lr at the path, in base

    path = path[1:]

    destination = os.path.join(base, path)
    if not os.path.exists(destination):
        os.makedirs(destination)

    # create an index contents.lr at each parent
    for part in path.split('/'):    # [:-1]:
        fp = os.path.join(base, 'contents.lr')
        print "Writing ", fp
        with open(fp, 'w') as f:
            f.write("_model: blog")

        base = os.path.join(base, part)

    outfile = os.path.join(destination, 'contents.lr')
    print "Writing", outfile
    with codecs.open(outfile, 'w', 'utf-8') as outf:
        outf.write(content)


def main():
    if not os.path.exists(OUT):
        os.makedirs(OUT)

    with open(IN) as f:
        xml = f.read()

    e = etree.fromstring(xml)
    for entry in e.xpath('//entry'):
        link = entry.xpath("field[@name='permaLink']")[0].text
        path = urlsplit(link)[2]

        write_lektor_document(OUT, path, lektorize(entry))


if __name__ == "__main__":
    main()
