+++
Tags = ["cookbook","Plone", "Zope", "Python"]
title = "Restore missing blobs from blob cache"
Description = ""
date = "Thu, 03 Aug 2017 13:40:28 GMT"
+++

I had a curious case of missing-but-present blobs in an old Plone service, configured with a Zeo server and 2 Zope instances. 

The root of the problem (I think) was that the blob folder configuration was broken: the Zope client instances were configured 
with shared blobs to "off", but they were really sharing the same caching folder. 

In the end, the blobs were loaded by the Zope services and everything appeared to be working, but when I've tried to move the 
blobstorage folder to a new machine, I ended up with missing blobs.

To tackle this problem, I wrote a quick migration view that will (given direct access to both folders, the caching folder and 
the real blobstorage) identify blobs that are present in the cache, convert their names to the one used by the bushy blob layout 
and copy them to the "proper" location. This could have been just a simple Python script, but easy enough to write it integrated
with Zope.

```python
class SyncBlobsFromCache(BrowserView):
    """ Sync blobs from the blobcache to the zeostorage blobstorage
    """

    def get_oid(self, foldername, filename):
        # 266, 208.03a01146df758b55.blob
        quot, enctid, _ignored = filename.split('.')
        oid = p64(int(quot) * 997 + int(foldername))
        tid = enctid.decode('hex')
        return oid, tid

    def __call__(self):
        # traverse all folders in configured cache location
        # the folder is the remainder of divmod(oid, 997)
        # the blob filename inside is in the following scheme:
        # rem/quot.<tid.encode('hex')>.blob

        conn = self.context._p_jar
        storage = conn._storage
        fshelper = storage.fshelper
        base_dir = fshelper.base_dir

        real_blobstoredir = os.path.join(base_dir, '../blobstorage')
        zeoblobsfshelper = FilesystemHelper(real_blobstoredir)

        cdirs = filter(lambda x: x and x.isdigit(),
                       [os.path.isdir(os.path.join(base_dir, x)) and x
                        for x in os.listdir(base_dir)])

        for dirname in cdirs:
            dpath = os.path.join(base_dir, dirname)
            blobnames = [x for x in os.listdir(dpath) if x.endswith('.blob')]
            for name in blobnames:
                oid, tid = self.get_oid(dirname, name)
                blobfilename = zeoblobsfshelper.getBlobFilename(oid, tid)
                if not os.path.exists(blobfilename):
                    cachefilename = fshelper.getBlobFilename(oid, tid)
                    fdirname = os.path.dirname(blobfilename)
                    if not os.path.exists(fdirname):
                        os.makedirs(fdirname)
                    shutil.copy(cachefilename, blobfilename)
                    logger.info("Copied blob from source %s to dest %s",
                                cachefilename, blobfilename)

        return "OK"

```
