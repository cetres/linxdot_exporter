class ExporterException(Exception):
    pass

class LoginFailedException(ExporterException):
    pass

class RequestException(ExporterException):
    pass