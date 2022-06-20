import csv
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


def has_pdf_link(session: BeautifulSoup):
    return len(session.find_all("a")) != 0


def main():
    ng_titles = []
    data = []
    links = get_nenji_proceeding_urls()
    for link in links:
        res = requests.get(link)
        soup = BeautifulSoup(res.content, "html.parser")
        sessions: list[BeautifulSoup] = soup.find_all("div", class_="session1")
        for session in sessions:
            if not has_pdf_link(session):
                continue

            title: BeautifulSoup | None = session.find("span", class_="session_title")
            if title is None:
                continue
            title_str: str = title.get_text()
            title_str = title_str.split(":")[-1]
            title_str = title_str.strip()

            is_ng = False
            for ng_title in ng_titles:
                if title_str.find(ng_title) != -1:
                    is_ng = True
                    break
            if is_ng:
                continue

            urls: list[BeautifulSoup] = session.find_all("a")
            for url in urls:
                url_str = url.get("href")
                if url_str == "#session_table":
                    continue
                url_str = urllib.parse.urljoin(link, url_str)
                data.append([title_str, url_str])

    with open("out.csv", "w", newline="", encoding="utf8") as f:
        writer = csv.writer(f)
        writer.writerows(data)


if __name__ == "__main__":
    main()
