def retry(f):
    """
    Decorator for API retrying.

    TOOD: not yet implemented.
    """
    def _inner(*args, **kwargs):
        return f(*args, **kwargs)
    return retry
