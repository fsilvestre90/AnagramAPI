# encoding: utf-8
"""
Extended Api implementation with an application-specific helpers
----------------------------------------------------------------
"""
from utilities import Api as BaseApi
from utilities import Namespace


class Api(BaseApi):
    """
    Having app-specific handlers here.
    """

    def namespace(self, *args, **kwargs):
        # The only purpose of this method is to pass custom Namespace class
        _namespace = Namespace(*args, **kwargs)
        self.namespaces.append(_namespace)
        return _namespace

    def add_namespace(self, ns):
        super(Api, self).add_namespace(ns)
