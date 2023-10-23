# settings/__init__.py
from typing import Any, List

from .base import DjangoSettings


_settings = DjangoSettings()
_settings_dict = _settings.model_dump()


def __dir__() -> List[str]:
    """The list of available options are retrieved from
    the dict view of our DjangoSettings object.
    """
    return list(_settings_dict.keys())


def __getattr__(name: str) -> Any:
    """Turn the module access into a DjangoSettings access"""
    return _settings_dict[name]
