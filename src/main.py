import re
import snscrape.modules.twitter as sntwitter
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

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
                cleanedTweet = removeTweetAts(tweet.rawContent)
                cleanedTweet = removeUrls(cleanedTweet)
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


# print()
app = FastAPI()

@app.get('/getUserTweets/{user}')
async def getUserTweets(user: str):
    return getTweets("martins_ikpe")

@app.get('/getUserTweets/{user}/{amount}')
async def getUserTweetsUpToAmount(user: str, amount: str):
    return getTweets("martins_ikpe", amount=int(amount))