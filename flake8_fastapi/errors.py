from flake8_plugin_utils import Error


class RouteDecoratorError(Error):
    code = "CF001"
    message = "Avoid `route` decorator. Use a suitable HTTP method as decorator."


class RouterPrefixError(Error):
    code = "CF002"
    message = (
        "Avoid using `prefix` parameter on `include_router`. "
        "Use it on the `Router` initialization."
    )


class GenericExceptionHandlerError(Error):
    code = "CF004"
    message = (
        "Don't try to handle `Exception` on the `exception_handler`. "
        "Create a new exception and handle that one, or use `HTTPException`."
    )


class CORSMiddlewareOrderError(Error):
    code = "CF008"
    message = (
        "The order of middleware matters, please use CORSMiddleware as the last one. "
        "Check https://github.com/tiangolo/fastapi/issues/1663 for more details."
    )


class NoContentResponseError(Error):
    code = "CF011"
    message = (
        "You need to add the `response_class` parameter on the decorator for 204. "
        "Example: '@app.get('/', status_code=204, response_class=Response)'."
    )
