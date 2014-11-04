import os
import hashlib
import pickle
import time
import sys
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


load_data()
new_tweets = 0

for tweet in filtered_tweets.values():
  tw_hash = hashlib.md5(tweet['text'].encode('utf8')).hexdigest()
  if tw_hash not in tweets_exported:
    tweets_exported[tw_hash] = ''
    raw_text = tweet['text'].encode('utf8')
    raw_text = ''.join(raw_text.split(','))
    raw_text = ''.join(raw_text.split('"'))
    text = ''.join(raw_text.split('\n'))
    csv.write('{0},{1},\n'.format(tweet['id'],text))
    new_tweets += 1

save_data()
csv.close()

if new_tweets == 0:
  os.system('rm {0}'.format(CSV_FILE))
  print 'Nothing to do.'
else:
  print 'Exported {0} tweets to csv/export_{1}.csv. Currently {2} tweets exported to drive.'\
  .format(new_tweets, TIME, len(tweets_exported))