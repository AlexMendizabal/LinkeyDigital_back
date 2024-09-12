from rest_framework.exceptions import APIException


class FirebaseAuthException(APIException):
    status_code = 500
    default_detail = 'Firebase Auth Exception'
    default_code = 'firebase_auth'


class TokenNotFound(APIException):
    status_code = 401
    default_detail = 'Credentials not found'
    default_code = 'token_not_found'


class InvalidToken(APIException):
    status_code = 401
    default_detail = 'Invalid Token'
    default_code = 'invalid_token'


class EmailNotVerified(APIException):
    status_code = 401
    default_detail = 'Email not Verified'
    default_code = 'email_not_verified'

class NotFound(APIException):
    status_code = 404
    default_detail = 'NOT FOUND'
    default_code = 'NOT_FOUND'

class Conflict(APIException):
    status_code = 409
    default_detail = 'Conflict'
    default_code = 'Conflict'