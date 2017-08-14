from app.extensions.api import api_v1


def init_app(app, **kwargs):
    # pylint: disable=unused-argument,unused-variable
    """
    Init words module.
    """
    # Touch underlying modules
    from . import models, resources

    api_v1.add_namespace(resources.words_ns)
    api_v1.add_namespace(resources.anagram_ns)
    api_v1.add_namespace(resources.palindrome_ns)
