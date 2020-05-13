import os
import uuid
import datetime

from django.utils import timezone


def get_today():
    return timezone.now().astimezone().date()


def get_uuid_filename(filename):
    """
    rename the file name to uuid4 and return the
    path
    """
    ext = filename.split('.')[-1]
    return "{}.{}".format(uuid.uuid4().hex, ext)


def get_upload_path(instance, filename):
    return os.path.join(f"uploads/{instance.__class__.__name__.lower()}",
                        get_uuid_filename(filename))
