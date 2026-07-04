import os
from datetime import datetime, timezone

import pandas as pd
import tweepy
from xquik_export import load_xquik_rows


def run_x_etl():
    username = os.getenv("X_USERNAME", "elonmusk")
    output_path = os.getenv("X_OUTPUT_PATH", "s3://airflow-bucket-yashreddie/elonmusk_tweets.csv")
    xquik_export_path = os.getenv("XQUIK_EXPORT_PATH")

    if xquik_export_path:
        df = pd.DataFrame(load_xquik_rows(xquik_export_path))
        df.to_csv(output_path, index=False)
        print(f"\nLoaded {len(df)} Xquik export rows for @{username}")
        return df

    bearer_token = os.getenv("X_BEARER_TOKEN", "")
    if not bearer_token or "PASTE_" in bearer_token:
        raise RuntimeError("Bearer Token is missing or not set")

    client = tweepy.Client(
        bearer_token=bearer_token,
        wait_on_rate_limit=True,
    )

    user_response = client.get_user(username=username)
    if user_response.data is None:
        raise RuntimeError(f"User '{username}' not found")

    tweets_response = client.get_users_tweets(
        id=user_response.data.id,
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
        user_fields=["username", "name"],
    )

    user_lookup = {}
    if tweets_response.includes and "users" in tweets_response.includes:
        for user in tweets_response.includes["users"]:
            user_lookup[user.id] = {
                "username": user.username,
                "name": user.name,
            }

    rows = []
    if tweets_response.data:
        for tweet in tweets_response.data:
            author = user_lookup.get(tweet.author_id, {})
            rows.append(
                {
                    "username": author.get("username"),
                    "text": tweet.text,
                    "created_at": tweet.created_at,
                    "lang": tweet.lang,
                    "like_count": tweet.public_metrics["like_count"],
                    "retweet_count": tweet.public_metrics["retweet_count"],
                    "reply_count": tweet.public_metrics["reply_count"],
                    "quote_count": tweet.public_metrics["quote_count"],
                    "extracted_at": datetime.now(timezone.utc),
                }
            )

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"\nFetched {len(df)} tweets for @{username}")
    return df
