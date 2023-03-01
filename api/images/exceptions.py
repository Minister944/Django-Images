from rest_framework.exceptions import APIException


class ExpiredLinkException(APIException):
    status_code = 403
    default_detail = "Link has expired."
    default_code = "link_has_expired"
