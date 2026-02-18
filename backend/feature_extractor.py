import re
from urllib.parse import urlparse
from normalize_url import normalize_url


def extract_features(url):

    url = normalize_url(url)

    # Ensure URL is string
    if not isinstance(url, str):
        url = ""

    features = []

    # 1️⃣ URL Length
    features.append(len(url))

    # 2️⃣ Number of dots
    features.append(url.count('.'))

    # 3️⃣ Contains @
    features.append(1 if "@" in url else 0)

    # 4️⃣ Contains IP address
    ip_pattern = r"(\d{1,3}\.){3}\d{1,3}"
    features.append(1 if re.search(ip_pattern, url) else 0)

    # 5️⃣ HTTPS usage
    features.append(1 if url.startswith("https") else 0)

    # 6️⃣ Suspicious keywords
    suspicious_keywords = [
        "login", "verify", "update", "secure",
        "bank", "account", "confirm", "password"
    ]
    features.append(
        sum(keyword in url.lower() for keyword in suspicious_keywords)
    )

    # 7️⃣ Number of hyphens
    features.append(url.count('-'))

    # 8️⃣ Number of slashes
    features.append(url.count('/'))

    # 9️⃣ Domain length & subdomain count
    try:
        domain = urlparse(url).netloc
    except:
        domain = ""

    features.append(len(domain))
    features.append(domain.count('.'))

    return features
