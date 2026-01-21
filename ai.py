from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os 
import pandas as pd

def analyze_title_ai(title):
    vs = analyzer.polarity_scores(title)
    score = vs['compound']
    
    category = "General"
    tags = {
        "Regulation": ["law", "sec", "legal", "court", "ban", "government"],
        "Tech": ["upgrade", "network", "fork", "security", "bug", "wallet"],
        "Market": ["price", "surge", "crash", "high", "low", "bull", "bear"]
    }
    
    for cat, keywords in tags.items():
        if any(word in title.lower() for word in keywords):
            category = cat
            break
            
    return score, category


def generate_market_summary(folder_path):
    summary_data = []
    
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(folder_path, file))
            coin_name = file.replace(".csv", "")
            
            summary_data.append({
                "crypto": coin_name,
                "sentiment_moyen": df['sentiment'].mean(),
                "nb_news": len(df),
                "stabilité_sentiment": df['sentiment'].std(), 
                "derniere_maj": datetime.now().strftime("%H:%M")
            })
    
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv("ai_market_summary.csv", index=False)
    print("🧠 Résumé IA généré dans ai_market_summary.csv")
