from email_sender import EmailSender
from stock_api import Stock, LimitExceeded
from news_api import News

COMPANY_NAME = "tcs"
STOCK_NAME = "TCS"

try:
    stock = Stock(STOCK_NAME)
    stock_performance = stock.performance()

    old_date = stock.day_before_yest_stock_date
    new_date = stock.yest_stock_date

    news = News(old_date, new_date, COMPANY_NAME)

    if stock_performance["status"]:
        email = EmailSender(STOCK_NAME, news.news, stock_performance["percentage"], "🔻")
    else:
        email = EmailSender(STOCK_NAME, news.news, stock_performance["percentage"], "▲")
except LimitExceeded as e:
    print(f"Error: {e}")