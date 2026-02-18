def normalize_url(url):
    if not isinstance(url, str):
        return ""
    url = url.lower().strip()
    if url.startswith("http://"):
        url = url[7:]
    if url.startswith("https://"):
        url = url[8:]
    if url.startswith("www."):
        url = url[4:]
    return url