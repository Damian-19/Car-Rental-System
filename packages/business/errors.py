# custom user-defined exceptions

class Error(Exception):
    """Default exception class"""
    pass


class MaxLoansReached(Error):
    """Raised when a user already has a vehicle on load"""
    pass
