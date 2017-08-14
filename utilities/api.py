from flask_restplus import Api as OriginalApi
from flask_restplus import Namespace
from flask_restplus import Swagger
from werkzeug.utils import cached_property


class Api(OriginalApi):
    @cached_property
    def __schema__(self):
        # The only purpose of this method is to pass custom Swagger class
        return Swagger(self).as_dict()

    def init_app(self, app):
        super(Api, self).init_app(app)

    def namespace(self, *args, **kwargs):
        # The only purpose of this method is to pass a custom Namespace class
        _namespace = Namespace(*args, **kwargs)
        self.add_namespace(_namespace)
        return _namespace

