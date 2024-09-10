# utils/context.py
# Thread-local storage for context
import threading
from contextlib import contextmanager

context = threading.local()


@contextmanager
def django_context():
    context.is_django = True
    yield
    context.is_django = False


@contextmanager
def celery_context():
    context.is_django = False
    yield


def is_celey_context():
    return not (hasattr(context, "is_django") and context.is_django)
