import feedparser
import pandas as pd
from datetime import datetime
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

def google_news(coin):
    url = f"https://news.google.com/rss/search?q={coin}+when:24h&hl=en-US&gl=US&ceid=US:en"
    
    feed = feedparser.parse(url)
    
    news_list = []
    
    for entry in feed.entries:
        news_list.append({
            "titre": entry.title,
            "lien": entry.link,
            "date": entry.published,
            "source": entry.source.title if hasattr(entry, 'source') else "Inconnue"
        })
    
    df = pd.DataFrame(news_list)
    file_path = os.path.join("crypto_storage", f"{coin}.csv")
    df.to_csv(file_path, index=False)
    return news_list


def coingacko_news():
    url = f"https://api.coingecko.com/api/v3/search/trending"
    headers = {
            "accept": "application/json"
    }
    response = requests.get(url, headers = headers)
    if response.status_code == 200:
         # Convert the JSON response to a Python dictionary
         data = response.json()

         # Extract relevant fields from the JSON data (coins section)
         coin_data = []
         for coin in data.get('coins', []):
            coin_item = coin.get('item', {})
            coin_data.append({
            'id': coin_item.get('id', ''),
            'name': coin_item.get('name', ''),
            'symbol': coin_item.get('symbol', ''),
            'market_cap_rank': coin_item.get('market_cap_rank', 0),
            'score': coin_item.get('score', 0)
        })

         df = pd.DataFrame(coin_data)
         df.to_csv('coingecko.csv', index = False)

    else:

         print(f"API request failed with status code: {response.status_code}")

def prepare_storage():
    """
    make the storage of crypto news more clean
    """
    folder_name = "crypto_storage"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

def get_trend_coins():
    """ 

    get the trending coins with coingecko to see the news and the rumors about the evolution of the market

    """
    file_path = 'coingecko.csv'
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        trend = df['id'].tolist()
        return trend
    else:
        print("Le fichier coingecko.csv n'existe pas encore.")
        return ["bitcoin", "ethereum", "solana", "cardano", "ripple"]



# Test script
prepare_storage()
coingacko_news() #getting trending coins in coingecko
trending = get_trend_coins()
for c in trending:
    google_news(c)

