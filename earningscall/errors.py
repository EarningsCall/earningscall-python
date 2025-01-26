class BaseError(RuntimeError):
    """
    Base error
    """

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        if self.msg:
            return str(self.msg)
        return ""


class ClientError(BaseError):
    """
    Used to return 4XX errors.
    """

    status: int = 400  # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400


class InsufficientApiAccessError(ClientError):
    pass


class InvalidApiKeyError(ClientError):
    pass
