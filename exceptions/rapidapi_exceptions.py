class ResponseIsEmptyError(BaseException):
    """Request to rapidapi doesn't return anything"""

    def __str__(self):
        return 'Server returned None'


class PageIndexError(IndexError):
    """Trying to get hotels page with index out of range"""

    def __str__(self):
        return 'Index of hotel page is out of range'


class BadRapidapiResultError(BaseException):
    """Request parametr "result" isn't OK"""

    def __str__(self):
        return 'Request parametr "result" is not OK'


class HotelsNotFoundError(BaseException):
    """Results list is empty"""

    def __str__(self):
        return 'Results list is empty'
