from datetime import datetime
import praw
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent="stock sentiment scraper by u/pixelizedgaming",
)

subreddits = {"stocks", "wallstreetbets", "investing", "daytrading"}
tickers = {"NVDA"}

def fetch_reddit_posts(subreddit_name, keyword, max_posts=100, timeframe="year"):
    subreddit = reddit.subreddit(subreddit_name)
    posts_data = []

    for submission in subreddit.search(keyword, limit=max_posts, time_filter=timeframe):
        posts_data.append({
            'date': datetime.fromtimestamp(submission.created_utc),
            'source': str(submission.author),
            'title': submission.title,
            'content': submission.selftext
        })

    return posts_data


if __name__ == "__main__":
    for subreddit_name in subreddits:
        for keyword in tickers:
            posts = fetch_reddit_posts(subreddit_name, keyword)

            df = pd.DataFrame(posts)
            df = df.drop_duplicates()
            df = df.dropna()
            df = df.sort_values(by="date")
            df.to_csv(f"out/r{subreddit_name}_{keyword}.csv", index=False)