"""
XCP Provider File Storage
"""


class FileStorage(object):
    """A simple NFS :class:`FileStorage` abstraction"""
    
    def __init__(self, config):
        pass

    def get_url(self, name):
        raise NotImplementedError()

    def get(self, name):
        raise NotImplementedError()

    def set(self, name):
        raise NotImplementedError()
