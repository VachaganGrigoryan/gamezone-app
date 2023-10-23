from functools import wraps
import inspect

from strawberry.types import Info


def required_(is_func, exc=ValueError):
    def decorator(func):

        get_result = getattr(func, 'get_result', None)
        if callable(get_result):
            func.get_result = decorator(func.get_result)

        sb_func = add_info(func)
        @wraps(sb_func)
        def wrapper(context, *args, **kwargs):
            context = context if context else kwargs.get('info').context
            if context and is_func(context.user):
                return handle_extra_kwargs(sb_func)(None, *args, **kwargs)
            raise exc
        return wrapper
    return decorator


login_required = required_(lambda user: user.is_authenticated)


def add_info(target):
    def signature(self, info: Info, *args, **kwargs):
        return target(*args, **kwargs)

    signature_inspections = inspect.signature(signature)
    if 'info' not in signature_inspections.parameters.keys():
        signature.__signature__ = inspect.Signature(
            parameters=[
                *signature_inspections.parameters.values(),
                inspect.Parameter('info', inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=Info)
            ],
            return_annotation=signature_inspections.return_annotation
        )
        signature.__annotations__ = target.__annotations__
        return signature
    return target


def handle_extra_kwargs(func):
    @wraps(func)
    def wrapper(src, *args_, **kwargs_):
        root = {}
        if src:
            args_ = args_[1:]

        present = inspect.signature(func).parameters.keys()
        for key, val in kwargs_.items():
            if key not in present:
                root[key] = val
        passed_kwargs = {k: v for k, v in kwargs_.items() if k in present}
        if src:
            return func(src, root, *args_, **passed_kwargs)
        if not root:
            return func(src, *args_, **passed_kwargs)
        return func(root, *args_, **passed_kwargs)
    return wrapper