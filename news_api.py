import dotenv
import html
import os
import requests

dotenv.load_dotenv()

URL = os.environ.get("NEWS_API_URL", "")
API_KEY = os.environ.get("NEWS_API_KEY", "")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


class News:
    def __init__(self, old_date: str, new_date: str, company_name: str):
        self.COMPANY_NAME = company_name
        self.news: list[dict[str, str]] = []
        self.old_date: str = old_date
        self.new_date: str = new_date

        self.get_news()

    def get_news(self):
        parameters = {
            "qInTitle": self.COMPANY_NAME,
            "pageSize": 3,
            "from": self.old_date,
            "to": self.new_date,
            "sortBy": "popularity"
        }

        response = requests.get(url=URL, headers=headers, params=parameters)
        response.raise_for_status()

        data = response.json()
        news_data = data["articles"]

        for news_dict in news_data:
            if len(self.news) < 3:
                self.news.append({
                    html.unescape(news_dict['title']): html.unescape(news_dict['description'] or "")
                })
            else:
                break

