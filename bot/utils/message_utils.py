from aiogram.utils import markdown as md


def build_detailed_message(
    *,
    title: str | None = None,
    details: list[tuple[str, str]],
    footer: str | None = None,
) -> str:
    content_title = md.html_decoration.bold(title) if title else ""
    content_details = md.text(*(f"{name}: {md.hbold(value)}" for name, value in details), sep="\n")
    content_footer = md.html_decoration.italic(footer) if footer else ""
    return md.text(content_title, content_details, content_footer, sep="\n\n")
