import feedparser
import pandas as pd
from datetime import datetime
import requests

def google_news(coin="bitcoin"):
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
    df.to_csv('google.csv', index=False)
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




# Test script
articles = google_news("bitcoin")
coingacko_news()
if not articles:
    print("Toujours rien... Vérifie ta connexion internet.")
else:
    print(f"✅ {len(articles)} articles trouvés via RSS !")
    for art in articles[:5]:
        print(f"- {art['titre']} ({art['source']})")