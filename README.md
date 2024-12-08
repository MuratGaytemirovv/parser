### **README.md**

#### **English**

# Parser Project

This project is a flexible and reusable web scraper designed to extract data from multiple websites based on custom configurations. The parser uses `BeautifulSoup` to scrape web pages and stores the extracted data in a structured JSON format.

## Features
- Dynamic configuration via `config.json`.
- Supports pagination for multi-page scraping.
- Extracts article titles and URLs from websites.
- Error handling and logging using Python's `logging` module.

## How to Use
1. Clone the repository:
   ```bash
   git clone https://github.com/MuratGaytemirovv/parser.git
   cd parser
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Update `config.json` with website-specific configurations.
4. Run the parser:
   ```bash
   python main.py
   ```
5. Extracted data will be saved in a JSON file named `<site_key>_articles.json`.

## Configuration
The `config.json` file contains selectors and URLs for each website. Example:
```json
{
    "news_ycombinator": {
        "base_url": "https://news.ycombinator.com",
        "pagination_url": "https://news.ycombinator.com/?p={page}",
        "article_selector": "td.title",
        "title_selector": "span.titleline a",
        "pagination_selector": "a.morelink"
    }
}
```

## Requirements
- Python 3.7 or higher
- `requests`
- `beautifulsoup4`

---

#### **Русский**

# Проект Парсер

Этот проект — гибкий и переиспользуемый веб-скраппер для извлечения данных с различных сайтов на основе пользовательских конфигураций. Парсер использует `BeautifulSoup` для обработки веб-страниц и сохраняет данные в формате JSON.

## Особенности
- Динамическая настройка через `config.json`.
- Поддержка пагинации для многостраничного скрапинга.
- Извлечение заголовков статей и ссылок.
- Обработка ошибок и логирование с использованием модуля `logging`.

## Как использовать
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/MuratGaytemirovv/parser.git
   cd parser
   ```
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Настройте `config.json` под нужный сайт.
4. Запустите парсер:
   ```bash
   python main.py
   ```
5. Извлеченные данные будут сохранены в JSON-файл с именем `<site_key>_articles.json`.

## Конфигурация
Файл `config.json` содержит селекторы и URL-адреса для каждого сайта. Пример:
```json
{
    "news_ycombinator": {
        "base_url": "https://news.ycombinator.com",
        "pagination_url": "https://news.ycombinator.com/?p={page}",
        "article_selector": "td.title",
        "title_selector": "span.titleline a",
        "pagination_selector": "a.morelink"
    }
}
```

## Требования
- Python 3.7 или выше
- `requests`
- `beautifulsoup4`

