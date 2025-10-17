import praw
from dotenv import load_dotenv
import os
import pandas as pd

d = {"Title": [], "Author": [], "Upvote": [], "URL": [], "text": []}


load_dotenv()
reddit = praw.Reddit(
    client_id=os.getenv("client_id"),
    client_secret=os.getenv("secret"),
    user_agent="motiv-agent-scaraper",
)

subreddit = reddit.subreddit(
    "software+mosttimeconsumingbusinessactivity+smallbusinessproblems"
)

for post in subreddit.hot(limit=400):

    title = post.title
    author = post.author
    upvote = post.score
    url = post.url
    text = post.selftext

    d["Title"].append(title)
    d["Author"].append(author)
    d["Upvote"].append(upvote)
    d["URL"].append(url)
    d["text"].append(text)


df = pd.DataFrame(data=d)

df.to_csv("business_idea.csv", index=False, encoding="UTF-8-sig")

print(f"Reddit found: {len(df)}")
