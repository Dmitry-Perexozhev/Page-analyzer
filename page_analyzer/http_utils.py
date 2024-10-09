import requests
import urllib3
from bs4 import BeautifulSoup


def url_parser(content) -> dict[str, None]:
    soup = BeautifulSoup(content, "html.parser")
    description_tag = soup.find("meta", attrs={"name": "description"})
    description_content = description_tag.get("content") if description_tag else None
    h1_content = soup.find("h1").get_text(strip=True) if soup.find("h1") else None
    title_content = soup.find("title").get_text(strip=True) if soup.find("title") else None
    return {'description': description_content,
            'h1': h1_content,
            'title': title_content}


def send_http_request(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except (requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            urllib3.exceptions.LocationParseError):
        raise RuntimeError
