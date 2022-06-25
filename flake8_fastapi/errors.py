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


class CORSMiddlewareOrderError(Error):
    code = "CF008"
    message = (
        "The order of middleware matters, please use CORSMiddleware as the last one. "
        "Check https://github.com/tiangolo/fastapi/issues/1663 for more details."
    )


class UndocumentedHTTPExceptionError(Error):
    code = "CF009"
    message = (
        "Always document your `HTTPException`s. "
        "Use the `responses` field on the router decorator for it."
    )


class NoContentResponseError(Error):
    code = "CF011"
    message = (
        "You need to add the `response_class` parameter on the decorator for 204. "
        "Example: '@app.get('/', status_code=204, response_class=Response)'."
    )
