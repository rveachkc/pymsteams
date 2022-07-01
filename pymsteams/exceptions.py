
class TeamsWebhookException(Exception):
    """custom exception for failed webhook call"""
    pass

class AsyncRequirementsMissing(Exception):
    """ raised when an async method is attempted without async requirements being met """