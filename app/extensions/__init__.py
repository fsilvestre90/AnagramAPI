# encoding: utf-8
# pylint: disable=invalid-name,wrong-import-position

"""
Extensions setup
================

Extensions provide access to common resources of the application.

Put new extension instantiations and initializations here.
"""
import os
from . import api

from config import BaseConfig
from local_config import LocalConfig

from walrus import Database

# redis = Database(host=LocalConfig.REDIS_HOST, port=LocalConfig.REDIS_PORT, db=LocalConfig.REDIS_DB)

redis = Database(host=BaseConfig.REDIS_HOST, password=BaseConfig.REDIS_PASSWORD)

def init_app(app):
    """
    Application extensions initialization.
    """

    for extension in (
            api,
    ):
        extension.init_app(app)
