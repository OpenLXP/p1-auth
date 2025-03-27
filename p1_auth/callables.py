from django.core.exceptions import PermissionDenied


def raise_error_if_email_not_validated(jwt_decoded, user, new):
    """
    If JWT does not contain `email_verified` with a value of True
    PermissionDenied is raised to cancel the request
    """
    if "email_verified" not in jwt_decoded or not \
            jwt_decoded["email_verified"]:
        raise PermissionDenied()
