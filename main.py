import os
import praw
from dotenv import load_dotenv

# Charge les variables du fichier .env
load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="CryptoSentinel v1.0"
)