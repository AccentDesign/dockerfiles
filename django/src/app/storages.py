from django.conf import settings as base_settings

from storages.backends.s3boto3 import S3Boto3Storage


class S3PrivateStorage(S3Boto3Storage):
    """
    A storage class that forcefully removes the custom domain
    This will force the class to revert back to the default s3 way of generating the urls
    with the querystring auth.
    acl='private' will mark the files as private when saving meaning
    the they will return an AccessDenied without the querystring auth.
    """

    def __init__(self, acl='private', bucket=None, **settings):
        settings.update({
            'custom_domain': None
        })
        super().__init__(acl, bucket, **settings)


class S3PublicStorage(S3Boto3Storage):
    """ Just subclass or use original class """

    def __init__(self, acl=None, bucket=None, **settings):
        settings.update({
            'querystring_auth': False
        })
        super().__init__(acl, bucket, **settings)


class S3StaticStorage(S3Boto3Storage):
    """ Stores files with the path prefix STATICFILES_LOCATION """

    def __init__(self, acl=None, bucket=None, **settings):
        settings.update({
            'querystring_auth': False,
            'location': base_settings.STATICFILES_LOCATION
        })
        super().__init__(acl, bucket, **settings)
