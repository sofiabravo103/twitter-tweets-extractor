import os
import hashlib
import pickle
import time
from information_mv import *

TWEETS_PICKLE_FILE = 'filtered_tweets.p'
TWEETS_IN_DRIVE_PICKLE_FILE = 'drive.p'
TIME = time.time()
CSV_FILE = 'export_{0}.csv'.format(TIME)

csv = open(CSV_FILE, 'w')

def load_data():
  global filtered_tweets
  global tweets_in_drive
  tweets_file = open(TWEETS_PICKLE_FILE,'rb')
  drive_file = open(TWEETS_IN_DRIVE_PICKLE_FILE,'rb')
  filtered_tweets = pickle.load(tweets_file)
  tweets_in_drive = pickle.load(drive_file)

def save_data():
  drive_file = open(TWEETS_IN_DRIVE_PICKLE_FILE,'wb')
  pickle.dump(tweets_in_drive, drive_file)


load_data()
new_tweets = 0

for tweet in filtered_tweets.values():
  tw_hash = hashlib.md5(tweet['text'].encode('utf8')).hexdigest()
  if tw_hash not in tweets_in_drive:
    tweets_in_drive[tw_hash] = ''
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
  print 'Exported {0} tweets to export_{1}.csv. Currently {2} tweets exported to drive.'\
  .format(new_tweets, TIME, len(tweets_in_drive))