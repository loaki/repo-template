# flake8: noqa

from project.store import store


__all__ = [
    "LOG_LEVEL",
    "LOG_MODE",
]

LOG_LEVEL = store.get_env_as_str(
    "LOG_LEVEL",
    "DEBUG",
    description="Log level (DEBUG, INFO, WARNING), default: DEBUG",
)

LOG_MODE = store.get_env_as_str(
    "LOG_MODE",
    "local",
    description="Log mode (local, production), default: local",
)
