class CarerentalError(Exception):
    def __init__(self, code, desc):
        self.code = code
        self.description = desc

    def __str__(self):
        return self.description


class clientBadRequestError(CarerentalError):
    def __init__(self, desc=None):
        self.code = 400
        self.description = "Bad Request" if desc is None else desc


class clientUnauthorizedError(CarerentalError):
    def __init__(self, desc=None):
        self.code = 401
        self.description = "Unauthorized" if desc is None else desc


class clientPaymentRequiredError(CarerentalError):
    def __init__(self, desc=None):
        self.code = 402
        self.description = "Payment Required" if desc is None else desc


class clientForbiddenError(CarerentalError):
    def __init__(self, desc=None):
        self.code = 403
        self.description = "Forbidden" if desc is None else desc


class clientNotFoundError(CarerentalError):
    def __init__(self, desc=None):
        self.code = 404
        self.description = "Not Found" if desc is None else desc


class clientMethodNotAllowedError(CarerentalError):
    def __init__(self, desc=None):
        self.code = 405
        self.description = "Method Not Allowed" if desc is None else desc


class clientNotAcceptableError(CarerentalError):
    def __init__(self, desc=None):
        self.code = 406
        self.description = "Not Acceptable" if desc is None else desc


class clientProxyAuthenticationRequiredError(CarerentalError):
    def __init__(self, desc=None):
        self.code = 407
        self.description = "Proxy Authentication Required" if desc is None else desc


class clientRequestTimeoutError(CarerentalError):
    def __init__(self, desc=None):
        self.code = 408
        self.description = "Request Timeout" if desc is None else desc


class clientConflictError(CarerentalError):
    def __init__(self, desc=None):
        self.code = 409
        self.description = "Conflict" if desc is None else desc


class clientGoneError(CarerentalError):
    def __init__(self, desc=None):
        self.code = 410
        self.description = "Gone" if desc is None else desc


class clientLengthRequiredError(CarerentalError):
    def __init__(self, desc=None):
        self.code = 411
        self.description = "Length Required" if desc is None else desc


class clientPreconditionFailedError(CarerentalError):
    def __init__(self, desc=None):
        self.code = 412
        self.description = "Precondition Failed" if desc is None else desc


class clientRequestEntityTooLargeError(CarerentalError):
    def __init__(self, desc=None):
        self.code = 413
        self.description = "Request Entity Too Large" if desc is None else desc


class clientRequestURITooLongError(CarerentalError):
    def __init__(self, desc=None):
        self.code = 414
        self.description = "Request-URI Too Long" if desc is None else desc


class clientUnsupportedMediaTypeError(CarerentalError):
    def __init__(self, desc=None):
        self.code = 415
        self.description = "Unsupported Media Type" if desc is None else desc


class clientRequestedRangeNotSatisfiableError(CarerentalError):
    def __init__(self, desc=None):
        self.code = 416
        self.description = "Requested Range Not Satisfiable" if desc is None else desc


class clientExpectationFailedError(CarerentalError):
    def __init__(self, desc=None):
        self.code = 417
        self.description = "Expectation Failed" if desc is None else desc


class serverInternalServerError(CarerentalError):
    def __init__(self, desc=None):
        self.code = 500
        self.description = "Internal Server Error" if desc is None else desc


class serverNotImplementedError(CarerentalError):
    def __init__(self, desc=None):
        self.code = 501
        self.description = "Not Implemented" if desc is None else desc


class serverBadGatewayError(CarerentalError):
    def __init__(self, desc=None):
        self.code = 502
        self.description = "Bad Gateway" if desc is None else desc


class serverServiceUnavailableError(CarerentalError):
    def __init__(self, desc=None):
        self.code = 503
        self.description = "Service Unavailable" if desc is None else desc


class serverGatewayTimeoutError(CarerentalError):
    def __init__(self, desc=None):
        self.code = 504
        self.description = "Gateway Timeout" if desc is None else desc


class serverHTTPVersionNotSupportedError(CarerentalError):
    def __init__(self, desc=None):
        self.code = 505
        self.description = "HTTP Version Not Supported" if desc is None else desc

