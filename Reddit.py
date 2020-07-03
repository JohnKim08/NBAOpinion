#! python3

#Funniest Comments 
import praw
import pandas as pd
import datetime as dt
from praw.models import MoreComments
from textblob import TextBlob
import re 
import nest_asyncio 
import numpy as np 

import requests 
import json 
import time 
import datetime 
import csv


ball = praw.Reddit(client_id='XABa6FL8_FKn2A', \
                     client_secret='6eqQMtSWufgR26l4hHPqjQzmveo', \
                     user_agent='NBAOpinion', \
                     username='TOBEFILLED', \
                     password='TOBEFILLED')

Thread = ball.subreddit('lakers')

#Trying to get this to work
#gamethread = Thread.


def getPushshiftData(query, after, before, sub):
    url = 'https://api.pushshift.io/reddit/search/submission/?title='+str(query)+'&size=1000&after='+str(after)+'&before='+str(before)+'&subreddit='+str(sub)
    print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']


def collectSubData(subm):
    subData = list() #list to store data points
    title = subm['title']
    url = subm['url']
    try:
        flair = subm['link_flair_text']
    except KeyError:
        flair = "NaN"    
    author = subm['author']
    sub_id = subm['id']
    score = subm['score']
    created = datetime.datetime.fromtimestamp(subm['created_utc']) #1520561700.0
    numComms = subm['num_comments']
    permalink = subm['permalink']
    subData.append((sub_id,title,url,author,score,created,numComms,permalink,flair))
    subStats[sub_id] = subData


sub = "lakers"
before = "1538352000"
after = "1514764800"
query = "[Post Game Thread]"
subCount = 0
subStats = {}
data = getPushshiftData(query, after, before, sub)
# Will run until all posts have been gathered 
# from the 'after' date up until before date
while len(data) > 0:
    for submission in data:
        collectSubData(submission)
        subCount+=1
    # Calls getPushshiftData() with the created date of the last submission
    print(len(data))
    print(str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])))
    after = data[-1]['created_utc']
    data = getPushshiftData(query, after, before, sub)
print(len(data))


print(str(len(subStats)) + " submissions have added to list")
print("1st entry is:")
print(list(subStats.values())[0][0][1] + " created: " + str(list(subStats.values())[0][0][5]))
print("Last entry is:")
print(list(subStats.values())[-1][0][1] + " created: " + str(list(subStats.values())[-1][0][5]))


def updateSubs_file():
    upload_count = 0
    filename = "NBA.csv"
    file = filename
    with open(file, 'w', newline='', encoding='utf-8') as file: 
        a = csv.writer(file, delimiter=',')
        headers = ["Post ID","Title","Url","Author","Score","Publish Date","Total No. of Comments","Permalink","Flair"]
        a.writerow(headers)
        for sub in subStats:
            a.writerow(subStats[sub][0])
            upload_count+=1
        print(str(upload_count) + " submissions have been uploaded")
        
    with open(file) as file:
        reader = csv.reader(file)
        header = next(reader)
        
        # Extract post ids
        ids = []
        for row in reader:
            id = row[0]
            ids.append(row)
    print(ids)
updateSubs_file() 


list1 = [] 
submission = ball.submission(id="en1gi2")
for comment in submission.comments:
  if isinstance(comment, MoreComments):
    continue
  list1.append(comment.body)

print(list1)


def clean_reddit(post):
  return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", post).split())
dataset = [clean_reddit(post) for post in list1]
dataset


def substring_search(comments, keyword):
    """Given list of comments, creates new list of comments that contain keyword"""
    new_list = [i for i in comments if keyword in i]
    return (new_list)


def get_reddit_sentiment(post):
  blob = TextBlob(post)
  if blob.sentiment.polarity >0:
    return 'positive'
  if blob.sentiment.polarity == 0:
    return 'neutral'
  return 'negative'
tweet_sentiments = [get_reddit_sentiment(post) for post in dataset]
tweet_sentiments[:10]


unique, counts = np.unique(tweet_sentiments,return_counts = True)
print(dict(zip(unique,counts)))
