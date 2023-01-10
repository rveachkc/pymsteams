from typing import Optional, Iterable, Tuple

TXT_BLOCK = "TextBlock"


def fmt_title_text(
    title_txt: str,
    weight: Optional[str] = "Bolder",
    size: Optional[str] = "Medium",
) -> dict:

    return {
        "type": TXT_BLOCK,
        "size": size,
        "weight": weight,
        "text": title_txt,
    }


def fmt_body_text(body_txt: str, wrap: Optional[bool] = True) -> dict:

    return {"type": TXT_BLOCK, "text": body_txt, "wrap": wrap}


def fmt_single_url(title: str, url: str) -> dict:

    return {
        "type": "Action.OpenUrl",
        "title": title,
        "url": url,
    }


def fmt_url_actions(urls: Iterable[Tuple[str, str]]) -> dict:

    return [fmt_single_url(x[0], x[1]) for x in urls]
