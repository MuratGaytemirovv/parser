import requests

from bs4 import BeautifulSoup as BS

url = "https://news.ycombinator.com"

articles = []


def get_articles(soup):
    trs = soup.find_all("tr", class_="submission")

    for tr in trs:
        span = tr.find("span", class_="titleline")
        if span:
            a = span.find("a")
            title = a.text
            url = a["href"]
            print(f"{title} <-- this article you can find on --> {url} \n\n")
            articles.append({"title": title, "url": url})


def get_soup(url):
    response = requests.get(url)
    if response.status_code == 200:
        html_doc = response.text
        soup = BS(html_doc, "html.parser")
    return soup


def get_pagination(soup):
    return soup.find("a", class_="morelink")


soup = get_soup(url=url)
if soup:
    pagination = get_pagination(soup)
    if pagination:
        page = 1
        while soup.find("td", class_="title"):
            url = f"https://news.ycombinator.com/?p={page}"
            soup = get_soup(url=url)
            get_articles(soup)
            page += 1

    else:
        get_articles(soup)


with open("articles.json", "w", encoding="utf-8") as f:
    import json

    json.dump(articles, f, indent=4, ensure_ascii=False)
