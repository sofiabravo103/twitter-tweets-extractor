#!/usr/bin/python2

import twitter
import hashlib
import pickle
import os
from information_spec import *

TWEETS_PICKLE_FILE = 'pickles/filtered_tweets.p'

def apply_filters(tweet):
  user = tweet['user']['screen_name']
  text = tweet['text']
  for rw in spec_rejected_keywords:
    if rw in text:
      return False
  for ru in spec_rejected_users:
    if ru in user:
      return False
  return True

def load_data():
  global filtered_tweets
  global last_id

  if not os.path.isdir('pickles'):
    os.makedirs('pickles')
    filtered_tweets = {}
  else:
    tweets_file = open(TWEETS_PICKLE_FILE,'rb')
    filtered_tweets = pickle.load(tweets_file)

def save_data():
  tweets_file = open(TWEETS_PICKLE_FILE,'wb')
  pickle.dump(filtered_tweets, tweets_file)

api = twitter.Api(
    consumer_key = spec_consumer_key,
    consumer_secret = spec_consumer_secret,
    access_token_key = spec_access_token,
    access_token_secret = spec_access_token_secret
)


unfiltered_tweets = []
unfiltered_dict_tweets = []

for u in spec_users:
  unfiltered_tweets += api.GetUserTimeline(screen_name=u, count=5000)

for ks in spec_keywords:
  for word in ks:
    unfiltered_tweets += api.GetSearch(term=word, count=5000)

load_data()

new_tweets = 0

for tw in unfiltered_tweets:
  unfiltered_dict_tweets.append(tw.AsDict())

for tw in unfiltered_dict_tweets:
  if retweeted_status_as_separate_tweet and 'retweeted_status' in tw:
    unfiltered_dict_tweets.append(tw['retweeted_status'])
    del tw['retweeted_status']

  tw['text'].encode('utf8')
  tw_hash = hashlib.md5(tw['text'].encode('utf8')).hexdigest()
  if tw_hash not in filtered_tweets:
    if apply_filters(tw):
      filtered_tweets[tw_hash] = tw
      new_tweets += 1

save_data()

if new_tweets == 0:
  print 'No new tweets, go eat a sandwich.'
elif new_tweets == 1:
  print 'Found just {0} new tweet! Current size is: {1}'\
  .format(new_tweets, len(filtered_tweets))
else:
  print 'Found {0} new tweets! Current size is: {1}'\
  .format(new_tweets, len(filtered_tweets))
