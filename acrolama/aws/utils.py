from django.core.files.storage import get_storage_class
from storages.backends.s3boto3 import S3Boto3Storage

"""
Documentation on:
and https://stackoverflow.com/questions/35417502/django-aws-s3-using-boto-with-compressor-fails-to-compress-uncompressablefileerr
"""


class CachedS3Boto3Storage(S3Boto3Storage):
    """
    S3 storage backend that saves files locally too.
    """

    location = "static"

    def __init__(self, *args, **kwargs):
        super(CachedS3Boto3Storage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class("compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        self.local_storage._save(name, content)
        super(CachedS3Boto3Storage, self).save(name, self.local_storage._open(name))
        return name


# StaticRootS3Boto3Storage = lambda: S3Boto3Storage(location='staticcollection')
MediaRootS3BotoStorage = lambda: S3Boto3Storage(location="media", file_overwrite="False")
