# -*- coding: utf-8 -*-
'''
Mercurial-based object store.

shove's URI for Mercurial-based stores follows the form:

hg://<path>

Where the path is a URI path to a Mercurial repository on a local filesystem.
Alternatively, a native pathname to the repository can be passed as the
'engine' argument.
'''

try:
    import hgapi
except ImportError:
    raise ImportError('requires hgapi library')

from shove.store import FileStore
from shove._compat import quote_plus


class HgStore(FileStore):

    init = 'hg://'

    def __init__(self, engine, **kw):
        super(HgStore, self).__init__(engine, **kw)
        self._repo = hgapi.Repo(self._dir)
        try:
            self._repo.hg_status()
        except Exception:
            self._repo.hg_init()

    def __setitem__(self, key, value):
        super(HgStore, self).__setitem__(key, value)
        fname = quote_plus(key)
#        if fname in self._repo.hg_status()['A']:
        self._repo.hg_add(fname)
        self._repo.hg_commit('added {0}'.format(fname))

    def __delitem__(self, key):
        super(HgStore, self).__delitem__(key)
        fname = quote_plus(key)
#        if fname in self._repo.hg_status()['R']:
        self._repo.hg_commit('removed {0}'.format(fname))
