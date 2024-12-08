import requests
from bs4 import BeautifulSoup as BS
import json
import logging

# Настройка логирования
logging.basicConfig(
    filename="parser.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# Чтение конфигурации из файла
def load_config(config_path="config.json"):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Файл конфигурации '{config_path}' не найден.")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Ошибка чтения JSON из файла '{config_path}': {e}")
        raise


articles = []


# Извлечение статей с текущей страницы
def get_articles(soup, config):
    """
    Извлекает статьи с текущей страницы на основе селекторов из конфигурации.
    """

    # Ищем все элементы, соответствующие article_selector
    elements = soup.select(config["article_selector"])
    for element in elements:
        # Используем title_selector для извлечения заголовков и ссылок
        link = element.select_one(config["title_selector"])
        if link:
            title = link.text.strip()
            url = link["href"]
            articles.append({"title": title, "url": url})
            logging.info(f"Найдена статья: '{title}' ({url})")
    return articles


# Функция для получения объекта BeautifulSoup для заданного URL
def get_soup(url):
    """
    Получает и парсит HTML-страницу по указанному URL.

    Args:
        url (str): URL для загрузки страницы.

    Returns:
        BeautifulSoup: Объект с разобранной HTML-страницей.
    """

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return BS(response.text, "html.parser")
        else:
            logging.warning(
                f"Не удалось загрузить страницу {url}: статус {response.status_code}"
            )
    except requests.RequestException as e:
        logging.error(f"Ошибка при запросе страницы {url}: {e}")
    return None


# Проверка наличия пагинации
def has_next_page(soup, config):
    """
    Проверяет наличие кнопки "следующая страница" на основе конфигурации.
    """
    return soup.select_one(config["pagination_selector"]) is not None


# Основная функция
def parse_site(site_key, config_path="config.json"):
    """
    Универсальный скрипт для работы с разными сайтами на основе конфигурации.
    """
    # Загружаем конфигурацию
    logging.info(f"Начало обработки сайта '{site_key}'")
    config = load_config(config_path).get(site_key)
    if not config:
        logging.error(f"Конфигурация для сайта '{site_key}' не найдена!")
        raise ValueError(f"Конфигурация для сайта '{site_key}' не найдена!")

    # Базовый URL и список для хранения статей
    base_url = config["base_url"]
    pagination_url = config["pagination_url"]
    articles = []

    # Первая страница
    page = 1
    url = base_url
    while True:
        logging.info(f"Загружаем страницу {page}: {url}")
        soup = get_soup(url)
        if not soup:
            logging.error(f"Не удалось загрузить страницу {page}. Останавливаемся.")
            break

        # Извлечение статей с текущей страницы
        articles.extend(get_articles(soup, config))

        # Проверка на наличие следующей страницы
        if not has_next_page(soup, config):
            logging.info("Страниц больше нет. Останавливаемся.")
            break

        # Формируем URL для следующей страницы
        page += 1
        url = pagination_url.format(page=page)

    # Сохраняем результаты в JSON-файл
    output_file = f"{site_key}_articles.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=4, ensure_ascii=False)
    logging.info(f"Статьи сохранены в файл {output_file}")


if __name__ == "__main__":
    parse_site("news_ycombinator")
