# custom user-defined exceptions

class Error(Exception):
    """Default exception class"""
    pass


class MaxLoansReached(Error):
    """Raised when a user already has a vehicle on load"""
    pass


class NegativeDaysReached(Error):
    """Raised when the user selects an end date before the start date"""
    pass
