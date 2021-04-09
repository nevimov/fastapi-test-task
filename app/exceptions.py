class BaseAppException(Exception):
    """Base class for the app's exceptions."""


class ReservedUrl(BaseAppException):
    """
    Raised when trying to add a URL with the same name as one of the site URL paths.
    """


class ShortUrlExists(BaseAppException):
    """
    Raised when trying to add a short URL that already exists in the database.

    Attributes:
        key -- The unique part of the short URL that when being prefixed
               with the scheme and the site domain makes a complete short
               URL. For example, in the https://shurl.me/sfH32HK string, the
               `key` wouldbe sfH32HK.
        message -- explanation of the error.
    """
    DEFAULT_MSG = (
        "Can't add a short URL with key: '{key}'. "
        "A URL with such key already exists in the database."
    )

    def __init__(self, key, message=None):
        self.key = key
        if message:
            self.message = message
        else:
            self.message = self.DEFAULT_MSG.format(key=key)


class UrlLimitExceeded(BaseAppException):
    """
    Raised when a user trying to add more short urls than is allowed by the
    USER_SHORTURL_LIMIT setting.
    """
