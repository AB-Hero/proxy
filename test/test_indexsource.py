from rezag.indexsource import FileIndexSource, RemoteIndexSource, MementoIndexSource, RedisIndexSource
from rezag.indexsource import LiveIndexSource

from rezag.aggindexsource import SimpleAggregator

from pywb.utils.timeutils import timestamp_now

from .testutils import key_ts_res


import pytest

import redis
import fakeredis

redis.StrictRedis = fakeredis.FakeStrictRedis
redis.Redis = fakeredis.FakeRedis

def setup_module():
    global r
    r = fakeredis.FakeStrictRedis(db=2)
    r.delete('test:rediscdx')
    with open('testdata/iana.cdxj', 'rb') as fh:
        for line in fh:
            r.zadd('test:rediscdx', 0, line.rstrip())


local_sources = [
    FileIndexSource('testdata/iana.cdxj'),
    RedisIndexSource('redis://localhost:6379/2/test:rediscdx')
]


remote_sources = [
    RemoteIndexSource('http://webenact.rhizome.org/all-cdx?url={url}',
                      'http://webenact.rhizome.org/all/{timestamp}id_/{url}'),

    MementoIndexSource('http://webenact.rhizome.org/all/{url}',
                       'http://webenact.rhizome.org/all/timemap/*/{url}',
                       'http://webenact.rhizome.org/all/{timestamp}id_/{url}')
]

ait_source = RemoteIndexSource('http://wayback.archive-it.org/cdx?url={url}',
                               'http://wayback.archive-it.org/all/{timestamp}id_/{url}')


def query_single_source(source, params):
    string = str(source)
    return SimpleAggregator({'source': source})(params)



# Url Match -- Local Loaders
# ============================================================================
@pytest.mark.parametrize("source", local_sources, ids=["file", "redis"])
def test_local_cdxj_loader(source):
    url = 'http://www.iana.org/_css/2013.1/fonts/Inconsolata.otf'
    res = query_single_source(source, dict(url=url, limit=3))

    expected = """\
org,iana)/_css/2013.1/fonts/inconsolata.otf 20140126200826 iana.warc.gz
org,iana)/_css/2013.1/fonts/inconsolata.otf 20140126200912 iana.warc.gz
org,iana)/_css/2013.1/fonts/inconsolata.otf 20140126200930 iana.warc.gz"""

    assert(key_ts_res(res) == expected)


# Closest -- Local Loaders
# ============================================================================
@pytest.mark.parametrize("source", local_sources, ids=["file", "redis"])
def test_local_closest_loader(source):
    url = 'http://www.iana.org/_css/2013.1/fonts/Inconsolata.otf'
    res = query_single_source(source, dict(url=url,
                  closest='20140126200930',
                  limit=3))

    expected = """\
org,iana)/_css/2013.1/fonts/inconsolata.otf 20140126200930 iana.warc.gz
org,iana)/_css/2013.1/fonts/inconsolata.otf 20140126200912 iana.warc.gz
org,iana)/_css/2013.1/fonts/inconsolata.otf 20140126200826 iana.warc.gz"""

    assert(key_ts_res(res) == expected)


# Prefix -- Local Loaders
# ============================================================================
@pytest.mark.parametrize("source", local_sources, ids=["file", "redis"])
def test_file_prefix_loader(source):
    res = query_single_source(source, dict(url='http://iana.org/domains/root/*'))

    expected = """\
org,iana)/domains/root/db 20140126200927 iana.warc.gz
org,iana)/domains/root/db 20140126200928 iana.warc.gz
org,iana)/domains/root/servers 20140126201227 iana.warc.gz"""

    assert(key_ts_res(res) == expected)


# Url Match -- Remote Loaders
# ============================================================================
@pytest.mark.parametrize("source", remote_sources, ids=["remote_cdx", "memento"])
def test_remote_loader(source):
    url = 'http://instagram.com/amaliaulman'
    res = query_single_source(source, dict(url=url))

    expected = """\
com,instagram)/amaliaulman 20141014150552 http://webenact.rhizome.org/all/20141014150552id_/http://instagram.com/amaliaulman
com,instagram)/amaliaulman 20141014155217 http://webenact.rhizome.org/all/20141014155217id_/http://instagram.com/amaliaulman
com,instagram)/amaliaulman 20141014162333 http://webenact.rhizome.org/all/20141014162333id_/http://instagram.com/amaliaulman
com,instagram)/amaliaulman 20141014171636 http://webenact.rhizome.org/all/20141014171636id_/http://instagram.com/amaliaulman"""

    assert(key_ts_res(res, 'load_url') == expected)


# Url Match -- Remote Loaders
# ============================================================================
@pytest.mark.parametrize("source", remote_sources, ids=["remote_cdx", "memento"])
def test_remote_closest_loader(source):
    url = 'http://instagram.com/amaliaulman'
    res = query_single_source(source, dict(url=url, closest='20141014162332', limit=1))

    expected = """\
com,instagram)/amaliaulman 20141014162333 http://webenact.rhizome.org/all/20141014162333id_/http://instagram.com/amaliaulman"""

    assert(key_ts_res(res, 'load_url') == expected)


# Url Match -- Memento
# ============================================================================
@pytest.mark.parametrize("source", remote_sources, ids=["remote_cdx", "memento"])
def test_remote_closest_loader(source):
    url = 'http://instagram.com/amaliaulman'
    res = query_single_source(source, dict(url=url, closest='20141014162332', limit=1))

    expected = """\
com,instagram)/amaliaulman 20141014162333 http://webenact.rhizome.org/all/20141014162333id_/http://instagram.com/amaliaulman"""

    assert(key_ts_res(res, 'load_url') == expected)

# Live Index -- No Load!
# ============================================================================
def test_live():
    url = 'http://example.com/'
    source = LiveIndexSource()
    res = query_single_source(source, dict(url=url))

    expected = 'com,example)/ {0} http://example.com/'.format(timestamp_now())

    assert(key_ts_res(res, 'load_url') == expected)




# Errors -- Not Found All
# ============================================================================
@pytest.mark.parametrize("source", local_sources + remote_sources, ids=["file", "redis", "remote_cdx", "memento"])
def test_all_not_found(source):
    url = 'http://x-not-found-x.notfound/'
    res = query_single_source(source, dict(url=url, limit=3))

    expected = ''
    assert(key_ts_res(res) == expected)


# ============================================================================
def test_another_remote_not_found():
    source = MementoIndexSource.from_timegate_url('http://www.webarchive.org.uk/wayback/archive/')
    url = 'http://x-not-found-x.notfound/'
    res = query_single_source(source, dict(url=url, limit=3))


    expected = ''
    assert(key_ts_res(res) == expected)


# ============================================================================
def test_file_not_found():
    source = FileIndexSource('testdata/not-found-x')
    url = 'http://x-not-found-x.notfound/'
    res = query_single_source(source, dict(url=url, limit=3))

    expected = ''
    assert(key_ts_res(res) == expected)


# ============================================================================
def test_ait_filters():
    ait_source = RemoteIndexSource('http://wayback.archive-it.org/cdx/search/cdx?url={url}&filter=filename:ARCHIVEIT-({colls})-.*',
                                   'http://wayback.archive-it.org/all/{timestamp}id_/{url}')

    cdxlist = query_single_source(ait_source, {'url': 'http://iana.org/', 'param.source.colls': '5610|933'})
    filenames = [cdx['filename'] for cdx in cdxlist]

    prefix = ('ARCHIVEIT-5610-', 'ARCHIVEIT-933-')

    assert(all([x.startswith(prefix) for x in filenames]))


    cdxlist = query_single_source(ait_source, {'url': 'http://iana.org/', 'param.source.colls': '1883|366|905'})
    filenames = [cdx['filename'] for cdx in cdxlist]

    prefix = ('ARCHIVEIT-1883-', 'ARCHIVEIT-366-', 'ARCHIVEIT-905-')

    assert(all([x.startswith(prefix) for x in filenames]))

