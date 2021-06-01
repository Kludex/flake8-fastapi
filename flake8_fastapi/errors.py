from flake8_plugin_utils import Error


class RouteDecoratorError(Error):
    code = "CF001"
    message = "Avoid `route` decorator. Use a suitable HTTP method as decorator."


class RouterPrefixError(Error):
    code = "CF002"
    message = (
        "Avoid using `prefix` parameter on `include_router`."
        "Use it on the `Router` initialization."
    )
