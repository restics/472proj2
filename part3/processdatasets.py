import pandas as pd

sentiment_scores = pd.read_csv("daily_sentiment_score.csv")
closing_prices = pd.read_csv("year_daily_NVDA_prices.csv")

# get sentiment scores from closing prices dates
sentiment_scores['date'] = pd.to_datetime(sentiment_scores['date'])
closing_prices['date'] = pd.to_datetime(closing_prices['date'])


# process sentiment scores
sentiment_scores['date'] = sentiment_scores['date'].dt.date
processed_sentiment_scores = sentiment_scores.groupby('date').mean().reset_index()
processed_sentiment_scores['date'] = pd.to_datetime(processed_sentiment_scores['date'])

print(processed_sentiment_scores)
new_df = closing_prices.copy()
new_df['change'] = closing_prices['close'].diff()
new_df = new_df.merge(processed_sentiment_scores, on='date', how='left').dropna(subset=['daily_sentiment_score'])
new_df = new_df[['change', 'daily_sentiment_score']]
new_df['change'] = new_df['change'].round(2)

new_df.to_csv("combined_sentiment_results.csv")

