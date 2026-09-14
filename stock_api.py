import os

import dotenv
import requests

dotenv.load_dotenv()

URL = os.environ.get("STOCK_API_URL", "")
API_KEY = os.environ.get("STOCK_API_KEY", "")

class LimitExceeded(Exception):
    pass

class Stock:
    def __init__(self, stock_name: str):
        self.STOCK_NAME = stock_name
        self.stock_details: list = []
        self.get_stock_data()
        self.yest_stock_date = " "
        self.day_before_yest_stock_date = " "

    def get_stock_data(self):
        parameters = {
            "apikey": API_KEY,
            "function": "TIME_SERIES_DAILY",
            "symbol": self.STOCK_NAME,
            "interval": "60min"
        }

        response = requests.get(URL, params=parameters)
        response.raise_for_status()

        stocks = response.json()
        try:
            stock_data = stocks["Time Series (Daily)"]

            c = 1
            for stock_date, stock_detail in stock_data.items():
                self.stock_details.append(
                    {
                        f"date": stock_date, f"open": float(stock_detail["1. open"]),
                        f"close": float(stock_detail["4. close"])
                    }
                )
                c += 1
                if c > 2:
                    break
            self.yest_stock_date = self.stock_details[1]["date"]
            self.day_before_yest_stock_date = self.stock_details[0]["date"]
        except KeyError:
            raise LimitExceeded("Stocks API limit reached")
        except IndexError:
            raise LimitExceeded("Stocks API limit reached")

    def performance(self):
        # NOTE: Percentage of the difference between yest stock closing and today's start price for new
        #  ((1000 - 900) / 900)) * 100
        # NOTE: ((new - old) / old) * 100

        new_stock = self.stock_details[0]["open"]
        old_stock = self.stock_details[1]["close"]
        is_bad = False

        stock_status = ((new_stock - old_stock) / old_stock) * 100

        if stock_status < -10:
            is_bad = True

        return {"status": is_bad, "message": f"Stock status: {stock_status}", "percentage": f"{stock_status:.2f}%"}


