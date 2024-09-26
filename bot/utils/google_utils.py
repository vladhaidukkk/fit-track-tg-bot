import urllib.parse


def generate_search_link(query: str) -> str:
    base_url = "https://www.google.com/search"
    params = {"q": query}
    return f"{base_url}?{urllib.parse.urlencode(params)}"
