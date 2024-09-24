from aiogram.utils import markdown as md


def build_detailed_message(
    *,
    title: str = "",
    details: list[tuple[str, str]],
    footer: str = "",
    bold_title: bool = True,
    numerate_details: bool = False,
    bold_detail_name: bool = True,
    bold_detail_value: bool = False,
    details_sep: str = "\n",
    italic_footer: bool = True,
) -> str:
    def build_detail(number: int, name: str, value: str) -> str:
        number_part = f"{number}. " if numerate_details else ""
        name_part = md.hbold(name) if bold_detail_name else name
        value_part = md.hbold(value) if bold_detail_value else value
        return f"{number_part}{name_part}: {value_part}"

    content_title = md.html_decoration.bold(title) if bold_title else title
    content_details = md.text(
        *(build_detail(number, name, value) for number, (name, value) in enumerate(details, start=1)),
        sep=details_sep,
    )
    content_footer = md.html_decoration.italic(footer) if italic_footer else footer
    return md.text(content_title, content_details, content_footer, sep="\n\n")
