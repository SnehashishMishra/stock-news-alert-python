import smtplib
import os, dotenv

dotenv.load_dotenv()

MY_EMAIL = os.environ.get('MY_EMAIL', '')
MY_PASSWORD = os.environ.get('MY_PASSWORD', '')
RECEIVER_EMAIL = os.environ.get('RECEIVER_EMAIL', '')

class EmailSender:
    def __init__(self, stock_name: str, news_list: list, down_perc: str, sign: str) -> None:
        self.STOCK_NAME = stock_name
        self.news: list = news_list
        self.down_perc: str = down_perc
        self.sign: str = sign

        self.send_email()

    def send_email(self) -> None:
        connection = smtplib.SMTP('smtp.gmail.com', 587)
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)

        for news in self.news:
            for title, description in news.items():
                msg =f"Subject: {self.STOCK_NAME} {self.down_perc} {self.sign}\n\nHeadline: {title}{'\nBrief: ' + description}"

                connection.sendmail(MY_EMAIL, RECEIVER_EMAIL, msg.encode('utf-8'))
