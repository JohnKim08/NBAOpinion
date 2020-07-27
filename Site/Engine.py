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

import application 

ball = praw.Reddit(client_id='yPIw50n6GcazPw', \
                     client_secret='U7m7nL_04ND6KgrGnwznkgTvCIY', \
                     user_agent='NBAOpinion', \
                     username='BallDontLie12', \
                     password='-')

player_name = "Lebron" 
team = "lakers"
if(team == "hawks"):
  sub = "AtlantaHawks"
if(team == "warrios"):
  sub = "warriors"
if(team == "lakers"):
  sub = "lakers"
if(team == "celtics"):
  sub = "bostonceltics"
if(team == "raptors"):
  sub = "torontoraptors"
if(team == "76ers"):
  sub = "sixers"
if(team =="bulls"):
  sub = "chicagobulls"
if(team == "rockets"):
  sub = "rockets"
if(team == "knicks"):
  sub = "NYKnicks"
if(team=="cavaliers"):
  sub = "clevelandcavs"
if(team == "thunder"):
  sub = "Thunder"
if(team == "bucks"):
  sub = "MkeBucks"
if(team == "mavericks"):
  sub = "mavericks"
if(team == "spurs"):
  sub = "NBASpurs"
if(team == "timberwolves"):
  sub = "timberwolves"
if(team == "wizards"):
  sub = "washingtonwizards"
if(team == "jazz"):
  sub = "UtahJazz"
if(team == "blazers"):
  sub = "ripcity"
if(team == "suns"):
  sub = "suns"
if(team=="kings"):
  sub = "kings"
if(team == "heat"):
  sub = "heat"
if(team == "nuggets"):
  sub = "denvernuggets"
if(team == "nets"):
  sub="GoNets"
if(team == "magic"):
  sub = "OrlandoMagic"
if(team == "pistons"):
  sub = "DetroitPistons"
if(team == "clippers"):
  sub = "LAClippers"
if(team == "pacers"):
  sub = "pacers"
if(team == "hornets"):
  sub = "CharlotteHornets"
if(team == "pelicans"):
  sub = "NOLAPelicans"
if(team == "grizzles" ):
  sub = "memphisgrizzlies"
  
before = "1538352000"
after = "1514764800"
Thread = ball.subreddit(sub)


# Have to get all the post ids of all post game threads 
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
    #print(len(data))
    #print(str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])))
    after = data[-1]['created_utc']
    data = getPushshiftData(query, after, before, sub)
ids = []

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
        #print(str(upload_count) + " submissions have been uploaded")
    df = pd.read_csv(filename)
    matrix2 = df[df.columns[0]].as_matrix()
    global ids 
    ids = matrix2.tolist()
    #with open(filename) as file:
      #ids = [row.split()[0] for row in file]
        #reader = csv.reader(file)
        #header = next(reader)
        
        # Extract post ids
        
        #for row in reader:
            #id = row[0]
            #ids.append(row)
    #print(ids)
updateSubs_file() 
#print(ids)
#iterate through the the list ids and also the comments through those posts


CommentText= []
for idcodes in range(len(ids)):
  submission = ball.submission(id = ids[idcodes])
  for comment in submission.comments:
    if isinstance(comment, MoreComments):
      continue
    CommentText.append(comment.body)

#print(ids)

def clean_reddit(post):
  return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", post).split())
dataset = [clean_reddit(post) for post in CommentText]
#dataset

def substring_search(comments, keyword):
    """Given list of comments, creates new list of comments that contain keyword"""
    new_list = [i for i in comments if keyword in i]
    return (new_list)
dataset = substring_search(dataset,player_name)

def get_reddit_sentiment(post):
  blob = TextBlob(post)
  if blob.sentiment.polarity >0:
    return 'positive'
  if blob.sentiment.polarity == 0:
    return 'neutral'
  return 'negative'


sentiments = [get_reddit_sentiment(post) for post in dataset]
unique, counts = np.unique(sentiments,return_counts = True)
print(dict(zip(unique,counts)))


