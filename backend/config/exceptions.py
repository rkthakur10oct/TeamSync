from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Global exception handler for TeamSync API.

    Converts DRF exceptions into a consistent JSON response format.
    """

    # Let Django REST Framework generate the standard response first.
    response = exception_handler(exc, context)

    # If DRF cannot handle the exception, return None.
    if response is None:
        return None

    data = response.data

    # Handle normal DRF exceptions such as:
    # 401, 403, 404, 405, etc.
    if isinstance(data, dict) and "detail" in data:
        message = str(data["detail"])
        errors = None

    # Handle serializer validation errors.
    # Example:
    # {
    #     "name": ["This field is required."]
    # }
    else:
        message = "Validation error"
        errors = data

    # Standard TeamSync error response.
    response.data = {
        "success": False,
        "status_code": response.status_code,
        "message": message,
        "errors": errors,
    }

    return response