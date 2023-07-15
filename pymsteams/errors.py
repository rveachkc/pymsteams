"""
pymsteams.errors
~~~~~~~~~~~~~~~~

A inner helper file to help Exception handlers.
"""

class TeamsException(BaseException):
    """
    Base class exception for all teams errors.
    """
    pass

class TeamsWebhookException(TeamsException):
    """
    Exception raised when a webhook call fails.
    """
    pass

class RateLimited(TeamsException):
    """
    Exception raised when the client is ratelimited.
    """

    def __init__(self, retry_after: float) -> None:
        super().__init__(
            f'Too many requests. Retry in {retry_after:.2f} seconds.'
        )