from urllib.parse import urlparse

import validators


def is_valid_url(url: str) -> bool:
    validator = validators.url(url)
    valid_len = len(url) < 255
    return validator and valid_len


def normalize_url(url: str) -> str:
    url_norm = urlparse(url)
    return url_norm.scheme + '://' + url_norm.netloc
