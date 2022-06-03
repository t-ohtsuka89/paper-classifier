import urllib.parse

import bs4
import requests
from bs4 import BeautifulSoup


def get_nenji_proceeding_urls() -> list[str]:
    res = requests.get("https://anlp.jp/guide/nenji_proceedings.html")
    soup = BeautifulSoup(res.content, "html.parser")

    links = [
        urllib.parse.urljoin(
            "https://anlp.jp/guide/nenji_proceedings.html", url.get("href")
        )
        for url in soup.find("div", class_="content_box").find_all("a")
    ]
    return links


def main():
    links = get_nenji_proceeding_urls()
    for link in links:
        res = requests.get(link)
        soup = BeautifulSoup(res.content, "html.parser")
        titles: bs4.element.ResultSet = soup.find_all("span", class_="session_title")
        for a in titles:
            print(a.get_text())


if __name__ == "__main__":
    main()
