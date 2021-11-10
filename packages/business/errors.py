# custom user-defined exceptions

class Error(Exception):
    """Default exception class"""
    pass


class ValueNotFoundError(Error):
    """Raised when a value is missing"""
    pass
