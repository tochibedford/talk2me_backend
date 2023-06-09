import re
import json
import sqlite3
from datetime import datetime
import snscrape.modules.twitter as sntwitter
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from database import insertUserTweets, updateUserTweets, getUserFromDB, createTweetsTable

DATA_EXPIRY_DURATION_IN_HOURS = 24
class TweetScrapeResult(BaseModel):
    status: int
    value: list[str]
    msg: Optional[str]

# removes all twitter handles from a tweet
def removeTweetAts(tweet: str):
    regexString = r'@[\w]+'
    return re.sub(regexString, "", tweet)

def removeUrls(tweet: str):
    regexString = r"http[s]?:\/\/([\/]?[\w.]+)+"
    return re.sub(regexString, "", tweet)

# returns not more than the given `amount` of tweets 
# promoted tweets and tweets that are empty after being cleaned are "skipped",
# hence the number of returned tweets isn't guaranteed to be up to `amount`
def getTweets(user: str, start: int = 0, amount: int = None) -> TweetScrapeResult:
    result = TweetScrapeResult(status=0, value=[])
    try:
        scraper = sntwitter.TwitterProfileScraper(user)
    except ValueError as e:
        result.status = 404
        result.msg = e.args[0]
        return result
    scraperGenerator = scraper.get_items() #this is a generator

    #skip index 0 to `start` tweets
    try:
        for i in range(start):
                next(scraperGenerator)
    except StopIteration:
        print("Reached end of tweets")
    finally:
        print("Finished Skips")

    count = 0
    for tweet in scraperGenerator:
        try:
            if not tweet.rawContent.startswith("RT"):
                cleanedTweet = removeUrls(tweet.rawContent)
                cleanedTweet = cleanedTweet.strip()
                if(cleanedTweet != ""): #skips tweets that are empty after cleaning
                    result.value.append(cleanedTweet)
                    count += 1
            if amount and count == amount-1:
                break
        except AttributeError:
            pass
    result.status = 200
    return result


# APIS AND DATABASE
app = FastAPI()
createTweetsTable()

origins = [
    "http://localhost:8000",
    "https://talk2me-frontend.vercel.app",
    "https://talk4me.vercel.app"
    "https://talk4me.tochibedford.com"
    "https://tochibedford.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)

@app.get('/getUserTweets/{user}')
def getUserTweets(user: str):
    dbTweetRecord = getUserFromDB(user)
    if dbTweetRecord:
        tweet_id,_,_,created_at = dbTweetRecord
        currentTime = datetime.utcnow()
        time_difference = currentTime.timestamp() - created_at.timestamp()
        if time_difference < DATA_EXPIRY_DURATION_IN_HOURS * 60 * 60:
            return json.loads(dbTweetRecord[2])
        else:
            try:
                tweets = getTweets(f"{user}")
            except:
                raise HTTPException(status_code=404, detail="User not found")
            if tweets.status == 404:
                    raise HTTPException(status_code=404, detail="User not found")
            updateUserTweets(user, json.dumps(tweets.value))
            return tweets.value
    else:
        try:
            tweets = getTweets(f"{user}")
        except:
            raise HTTPException(status_code=404, detail="User not found")
        if tweets.status == 404:
                raise HTTPException(status_code=404, detail="User not found")
        insertUserTweets(user, json.dumps(tweets.value))
        return tweets.value

@app.get('/getUserTweets/{user}/{amount}')
def getUserTweetsUpToAmount(user: str, amount: str):
    dbTweetRecord = getUserFromDB(user)
    if dbTweetRecord:
        tweet_id,_,_,created_at = dbTweetRecord
        currentTime = datetime.utcnow()
        time_difference = currentTime.timestamp() - created_at.timestamp()
        if time_difference < DATA_EXPIRY_DURATION_IN_HOURS * 60 * 60:
            return json.loads(dbTweetRecord[2])
        else:
            try:
                tweets = getTweets(f"{user}", amount=int(amount))
            except:
                raise HTTPException(status_code=404, detail="User not found")
            if tweets.status == 404:
                raise HTTPException(status_code=404, detail="User not found")
            updateUserTweets(user, json.dumps(tweets.value))
            return tweets.value
    else:
        try:
            tweets = getTweets(f"{user}", amount=int(amount))
        except:
            raise HTTPException(status_code=404, detail="User not found")
        if tweets.status == 404:
            raise HTTPException(status_code=404, detail="User not found")
        insertUserTweets(user, json.dumps(tweets.value))
        return tweets.value