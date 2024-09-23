import re

import inflect

inflector = inflect.engine()


def pascal_to_snake(text: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", text).lower()


def pluralize(text: str) -> str:
    plural_form = inflector.plural_noun(text)
    return text if plural_form.endswith("ss") else plural_form


def get_tail(text: str) -> str:
    parts = text.split(maxsplit=1)
    return parts[-1] if parts else ""
