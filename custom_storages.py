from django.conf import settings
from storages.backends.s3boto import S3BotoStorage


class StaticStorage(S3BotoStorage):
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3BotoStorage):
    location = settings.MEDIAFILES_LOCATION


class CachedS3BotoStorage(S3BotoStorage):
    location = settings.COMPRESS_LOCATION
