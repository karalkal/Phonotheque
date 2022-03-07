from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class CheckMaxSizeInMb:
    MAX_PERMITTED_SIZE_IN_MB = 4

    def __init__(self, max_size=MAX_PERMITTED_SIZE_IN_MB):
        self.max_size = max_size

    def __call__(self, value):
        filesize = value.file.size
        if filesize > self.max_size * 1024 * 1024:
            raise ValidationError('Max file size is 4.00 MB')
