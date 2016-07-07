#!/usr/bin/python2

import os
import hashlib
import pickle
import time
import sys
import re
from information_spec import *

TWEETS_PICKLE_FILE = 'pickles/filtered_tweets.p'
TWEETS_EXPORTED_PICKLE_FILE = 'pickles/exported_tweets.p'
TIME = time.time()
CSV_FILE = 'csv/export_{0}.csv'.format(TIME)


def load_data():
  global filtered_tweets
  global tweets_exported
  global csv

  if not os.path.isdir('pickles'):
    print 'Please run find_tweets first, I have nothing to export!'
    sys.exit()

  if not os.path.isdir('csv'):
    os.makedirs('csv')
    tweets_exported = {}
  else:
    exports_file = open(TWEETS_EXPORTED_PICKLE_FILE,'rb')
    tweets_exported = pickle.load(exports_file)

  csv = open(CSV_FILE, 'w')
  tweets_file = open(TWEETS_PICKLE_FILE,'rb')
  filtered_tweets = pickle.load(tweets_file)


def save_data():
  drive_file = open(TWEETS_EXPORTED_PICKLE_FILE,'wb')
  pickle.dump(tweets_exported, drive_file)


def remove_separator(element):
  try:
    # case: element is a hash
    for key in element.keys():
      element[key] = remove_separator(element[key])
  except AttributeError:
    try:
      # case: element is a str
      element = re.sub(';', '', element)
    except TypeError:
      # case: element is not a hash nor a str
      try:
        # case: element is a list
        for item in element:
          item = remove_separator(item)
      except TypeError:
        # bool o number
        # don't do anything
        pass

  return element


load_data()
new_tweets = 0

for tweet in filtered_tweets.values():
  remove_separator(tweet)

  # export only new tweets
  tw_hash = hashlib.md5(tweet['text'].encode('utf8')).hexdigest()
  if tw_hash not in tweets_exported:
    tweets_exported[tw_hash] = ''

    # tweet info proccesing
    first = True
    for key in tweet.keys():
      if not first:
        csv.write(';')
      else:
        first = False

      try:
        raw_text = tweet[key].encode('utf8')

        # remove characters , : " ' and \n
        raw_text = ''.join(raw_text.split(','))
        raw_text = ''.join(raw_text.split(':'))
        raw_text = ''.join(raw_text.split('"'))
        raw_text = ''.join(raw_text.split("'"))
        text = ''.join(raw_text.split('\n'))
        csv.write('{0}:{1}'.format(key, text))
      except AttributeError:
        # attribute is not a string so don't process it
        csv.write('{0}:{1}'.format(key, tweet[key]))

    csv.write('\n')
    new_tweets += 1


save_data()
csv.close()

if new_tweets == 0:
  os.system('rm {0}'.format(CSV_FILE))
  print 'Nothing to do.'
else:
  print 'Exported {0} tweets to csv/export_{1}.csv. Currently {2} tweets exported.'\
  .format(new_tweets, TIME, len(tweets_exported))
