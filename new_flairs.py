import praw
import sys
from tokens import *
from team_conversion import *

code = input("2fa code? ")
pwd = MOD_PWD
if len(code) > 0:
    pwd = MOD_PWD + ":" + code

r = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent="finder-bot",
    username=MOD,
    password=pwd)

subreddit = r.subreddit("dota2")

LOG = open("log/conversion.log", "a")

users = set()
for f in subreddit.flair(limit=None):
    flair_class_class = f["flair_css_class"]
    if not flair_class_class or flair_class_class not in CSS_TO_EMOTE:
        continue

    flair_text = "" if f["flair_text"] is None else f["flair_text"]
    emote = CSS_TO_EMOTE[flair_class_class]

    if emote not in flair_text:
        new_text = emote + " " + flair_text.strip()
        username = f["user"].name
        subreddit.flair.set(
            username,
            text=new_text.strip(),
            css_class=flair_class_class)
        LOG.write(str(f) + "\n")
        users.add(username)

    if len(users) % 25 == 0 and len(users) > 0:
        LOG.flush()
        print(len(users))

LOG.close()
