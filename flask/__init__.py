from typing import Any, Callable, Dict, List, Optional, Tuple


class Session(dict):
    pass


session = Session()


class Request:
    def __init__(self, form: Optional[Dict[str, Any]] = None):
        self.form = form or {}

    def get(self, key: str, default=None):
        return self.form.get(key, default)

    def set_form(self, form: Dict[str, Any]):
        self.form = form


class Response:
    def __init__(self, data: Any = "", status_code: int = 200, headers: Optional[Dict[str, str]] = None):
        self.data = data
        self.status_code = status_code
        self.headers = headers or {}


class Blueprint:
    def __init__(self, name: str, import_name: str):
        self.name = name
        self.import_name = import_name
        self.routes: List[Tuple[str, List[str], Callable]] = []

    def route(self, rule: str, methods: Optional[List[str]] = None):
        methods = methods or ["GET"]

        def decorator(func: Callable):
            self.routes.append((rule, methods, func))
            return func

        return decorator


request = Request()


class Flask:
    def __init__(self, import_name: str):
        self.import_name = import_name
        self._routes: List[Tuple[str, List[str], Callable, str]] = []
        self.config: Dict[str, Any] = {}
        self.jinja_env = type("JinjaEnv", (), {"globals": {}})()

    def register_blueprint(self, blueprint: Blueprint, url_prefix: str = ""):
        for rule, methods, func in blueprint.routes:
            endpoint = f"{blueprint.name}.{func.__name__}"
            full_rule = f"{url_prefix}{rule}" or "/"
            self._routes.append((full_rule, methods, func, endpoint))

    def route(self, rule: str, methods: Optional[List[str]] = None):
        methods = methods or ["GET"]

        def decorator(func: Callable):
            self._routes.append((rule, methods, func, func.__name__))
            return func

        return decorator

    def test_client(self):
        return TestClient(self)

    def _match(self, path: str, method: str):
        for rule, methods, func, endpoint in self._routes:
            params = _match_rule(rule, path)
            if params is not None and method.upper() in methods:
                return func, params, endpoint
        return None, None, None


class TestClient:
    def __init__(self, app: Flask):
        self.app = app

    def get(self, path: str, follow_redirects: bool = False):
        return self._execute("GET", path, {}, follow_redirects)

    def post(self, path: str, data: Optional[Dict[str, Any]] = None, follow_redirects: bool = False):
        return self._execute("POST", path, data or {}, follow_redirects)

    def _execute(self, method: str, path: str, form: Dict[str, Any], follow_redirects: bool):
        func, params, _ = self.app._match(path, method)
        if func is None:
            return Response(status_code=404)
        request.set_form(form)
        result = func(**(params or {})) if params else func()
        if isinstance(result, Response):
            response = result
        else:
            response = Response(data=result, status_code=200)
        if follow_redirects and response.status_code in (301, 302) and "Location" in response.headers:
            return self.get(response.headers["Location"], follow_redirects=True)
        return response


def render_template(template_name: str, **context):
    return f"Rendered {template_name} with {context}"


def redirect(location: str):
    return Response(status_code=302, headers={"Location": location})


def abort(status_code: int):
    return Response(status_code=status_code)


def url_for(endpoint: str, **values):
    if endpoint == "todo.index":
        return "/"
    for key, val in values.items():
        if key in endpoint:
            return str(val)
    return "/"


def _match_rule(rule: str, path: str):
    rule_parts = [part for part in rule.strip("/").split("/") if part or rule == "/"]
    path_parts = [part for part in path.strip("/").split("/") if part]
    if rule == "/":
        return {} if path in ("/", "") else None
    if len(rule_parts) != len(path_parts):
        return None
    params = {}
    for rule_part, path_part in zip(rule_parts, path_parts):
        if rule_part.startswith("<int:") and rule_part.endswith(">"):
            name = rule_part[5:-1]
            try:
                params[name] = int(path_part)
            except ValueError:
                return None
        elif rule_part == path_part:
            continue
        else:
            return None
    return params


__all__ = [
    "Flask",
    "Blueprint",
    "render_template",
    "request",
    "redirect",
    "url_for",
    "session",
    "abort",
]
