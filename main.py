import feedparser
import pandas as pd
from datetime import datetime

def get_cryptonew_google(coin="bitcoin"):
    # URL RSS officielle de Google News pour le mot-clé
    url = f"https://news.google.com/rss/search?q={coin}+when:24h&hl=en-US&gl=US&ceid=US:en"
    
    # On "parse" le flux
    feed = feedparser.parse(url)
    
    news_list = []
    
    for entry in feed.entries:
        news_list.append({
            "titre": entry.title,
            "lien": entry.link,
            "date": entry.published,
            "source": entry.source.title if hasattr(entry, 'source') else "Inconnue"
        })
    
    return news_list





# Test du script
articles = get_crypto_news_rss("bitcoin")

if not articles:
    print("Toujours rien... Vérifie ta connexion internet.")
else:
    print(f"✅ {len(articles)} articles trouvés via RSS !")
    for art in articles[:5]:
        print(f"- {art['titre']} ({art['source']})")