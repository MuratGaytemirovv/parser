import requests

from bs4 import BeautifulSoup as BS

url = "https://news.ycombinator.com"

articles = []


# Функция для извлечения статей из текущей страницы
def get_articles(soup):
    """
    Извлекает заголовки и ссылки на статьи из текущей страницы.

    Args:
        soup (BeautifulSoup): Объект BeautifulSoup с разобранной HTML-страницей.

    Returns:
        None. Добавляет статьи в глобальный список `articles`.
    """
    trs = soup.find_all("tr", class_="submission")

    for tr in trs:
        span = tr.find("span", class_="titleline")
        if span:
            a = span.find("a")
            title = a.text
            url = a["href"]
            print(f"{title} <-- this article you can find on --> {url} \n\n")
            articles.append({"title": title, "url": url})


# Функция для получения объекта BeautifulSoup для заданного URL
def get_soup(url):
    """
    Получает и парсит HTML-страницу по указанному URL.

    Args:
        url (str): URL для загрузки страницы.

    Returns:
        BeautifulSoup: Объект с разобранной HTML-страницей.
    """

    response = requests.get(url)
    if response.status_code == 200:
        html_doc = response.text
        soup = BS(html_doc, "html.parser")
    return soup


# Функция для проверки наличия кнопки "More"
def get_pagination(soup):
    """
    Проверяет, есть ли на текущей странице кнопка "More" для перехода к следующей.

    Args:
        soup (BeautifulSoup): Объект BeautifulSoup с разобранной HTML-страницей.

    Returns:
        Tag or None: Ссылка на кнопку "More", если она существует.
    """
    return soup.find("a", class_="morelink")


# Получаем объект BeautifulSoup для первой страницы
soup = get_soup(url=url)
# Проверяем наличие кнопки "More" для пагинации
if soup:
    pagination = get_pagination(soup)
    if pagination:
        page = 1  # Начинаем с первой страницы
        while soup.find("td", class_="title"):  # Пока есть статьи на странице
            # Формируем URL для следующей страницы
            url = f"https://news.ycombinator.com/?p={page}"
            # Загружаем и парсим следующую страницу
            soup = get_soup(url=url)
            # Извлекаем статьи с текущей страницы
            get_articles(soup)
            page += 1

    else:
        # Если пагинации нет, просто извлекаем статьи с первой страницы
        get_articles(soup)

# Сохраняем извлеченные статьи в файл JSON
# with open("articles.json", "w", encoding="utf-8") as f:
#     import json

#     json.dump(articles, f, indent=4, ensure_ascii=False)
