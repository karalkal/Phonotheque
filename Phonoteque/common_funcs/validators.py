from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class MaxSizeInMbValidator:
    MAX_PERMITTED_SIZE_IN_MB = 1

    def __init__(self, max_size=MAX_PERMITTED_SIZE_IN_MB):
        self.max_size = max_size

    def __call__(self, value, max_size=MAX_PERMITTED_SIZE_IN_MB):
        filesize = value.file.size
        if filesize > self.max_size * 1024 * 1024:
            raise ValidationError(f'Max permitted image file size is {max_size}.00 MB')

