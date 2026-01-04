import tweepy
import pandas as pd
from datetime import datetime, timezone

# -------------------------------------------------------------------
# X API v2 Bearer Token (READ-ONLY ACCESS)
# -------------------------------------------------------------------
# IMPORTANT: Replace this with your actual Bearer Token
# Developer Portal → Projects & Apps → Your App → Keys and Tokens
# -------------------------------------------------------------------

def run_x_etl():

    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAC8G6wEAAAAAQe3m315xvCbqH6cqrYF9C35ytd4%3DTsBTsuIdgTMMnVFvV3O0llFsjqm5MJtquRViMH0mXV0F75ppcP"

    if not BEARER_TOKEN or "PASTE_" in BEARER_TOKEN:
        raise RuntimeError("Bearer Token is missing or not set")

    # -------------------------------------------------------------------
    # Create X API v2 Client (Bearer Token auth)
    # -------------------------------------------------------------------
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        wait_on_rate_limit=True,
    )

    # -------------------------------------------------------------------
    # Fetch user ID from username
    # -------------------------------------------------------------------
    USERNAME = "elonmusk"

    user_response = client.get_user(username=USERNAME)

    if user_response.data is None:
        raise RuntimeError(f"User '{USERNAME}' not found")

    user_id = user_response.data.id

    # -------------------------------------------------------------------
    # Fetch recent tweets (v2 endpoint, free-tier compatible)
    # -------------------------------------------------------------------
    tweets_response = client.get_users_tweets(
        id=user_id,
        max_results=20,
        exclude=["retweets", "replies"],
        tweet_fields=[
            "id",
            "text",
            "created_at",
            "lang",
            "public_metrics",
            "author_id",
        ],
        user_fields=[
            "username", "name"],
    )

    user_lookup = {}

    if tweets_response.includes and "users" in tweets_response.includes:
        for user in tweets_response.includes["users"]:
            user_lookup[user.id] = {
                "username": user.username,
                "name": user.name,
            }


    # -------------------------------------------------------------------
    # Normalize response into a Pandas DataFrame
    # -------------------------------------------------------------------
    rows = []

    if tweets_response.data:
        for tweet in tweets_response.data:
            author = user_lookup.get(tweet.author_id, {})
            rows.append({
                "username": author.get("username"),
                "text": tweet.text,
                "created_at": tweet.created_at,
                "lang": tweet.lang,
                "like_count": tweet.public_metrics["like_count"],
                "retweet_count": tweet.public_metrics["retweet_count"],
                "reply_count": tweet.public_metrics["reply_count"],
                "quote_count": tweet.public_metrics["quote_count"],
                "extracted_at": datetime.now(timezone.utc),
            })

    df = pd.DataFrame(rows)
    df.to_csv("s3://airflow-bucket-yashreddie/elonmusk_tweets.csv", index=False)

# -------------------------------------------------------------------
# Output
# -------------------------------------------------------------------
print(df)
print(f"\nFetched {len(df)} tweets for @{USERNAME}")
