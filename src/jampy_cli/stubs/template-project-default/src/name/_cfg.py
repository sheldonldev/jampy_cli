import importlib.metadata

APP_NAME = "temp_project"
__info__ = importlib.metadata.metadata(APP_NAME)

VERSION = __info__.get("version")
AUTHOR_EMAIL = __info__.get("author_email")
