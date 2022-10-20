import requests
from datetime import datetime, timedelta
import os
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
stock_key = 'R27OZ888UTHRRDM5'
news_key = '340a9eb54880435fa04ce5374ded7378'

account_sid = 'AC63bdae5fc8e901f24fa9d8bd0c5ef901'
auth_token = '157fb13d1582e5953e80606e2ea911d2'

stock_parameters = {
    "function": 'TIME_SERIES_DAILY',
    "symbol": STOCK_NAME,
    "apikey": stock_key,
}

response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
stock_data = (response.json()['Time Series (Daily)'])
# Calculates dates
yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
day_before_yesterday = (datetime.now() - timedelta(2)).strftime('%Y-%m-%d')
# Retrieves closing prices
yesterday_close = float(stock_data[yesterday]['4. close'])
day_before_yesterday_close = float(stock_data[day_before_yesterday]['4. close'])

positive_difference = round((day_before_yesterday_close - yesterday_close) * -1, 2)

percent_diff = round((positive_difference / day_before_yesterday_close) * 100, 2)
print(percent_diff)

news_parameters = {
    "q": f'+{STOCK_NAME}',
    "from": (datetime.now() - timedelta(3)).strftime('%Y-%m-%d'),
    'to': yesterday,
    "apikey": news_key,
    'language': 'en',
    'sortBy': 'popularity'
}

response = requests.get(NEWS_ENDPOINT, params=news_parameters)
news_data = (response.json())
articles = (news_data['articles'][:3])
# Sends links to articles if stock plummets more than 5% or increases more than 5% to a phone number
if percent_diff > 5:
    article_list = [
        f"{STOCK_NAME}: ▲️{percent_diff} \nHeadline: {article['title']} \nBrief: {article['description']} \nLink: {article['url']} "
        for
        article in articles]
    for article_info in article_list:
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body=article_info,
            from_='+19785043248',
            to='+16477123349'
        )

        print(message.sid)
elif percent_diff < -5:
    article_list = [
        f"{STOCK_NAME}: 🔻️️{percent_diff} \nHeadline: {article['title']} \nBrief: {article['description']} \nLink: {article['url']} "
        for
        article in articles]

    for article_info in article_list:
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body=article_info,
            from_='+19785043248',
            to='+16477123349'
        )

        print(message.sid)
else:

    print(None)
