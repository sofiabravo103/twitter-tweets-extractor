import twitter
import hashlib
import pickle
from information_mv import *

TWEETS_PICKLE_FILE = 'filtered_tweets.p'

def apply_filters(tweet):
  rejected_keywords = ['cola', 'trafico', 'carro', 'gandola', 'avenida',\
  'protesta','perro','mascota','desaparecido','desaparecida']
  rejected_users = ['traffic', 'aquivendo','currentlyes','elnacionalweb']
  user = tweet.user.screen_name
  text = tweet.text
  for rw in rejected_keywords:
    if rw in text:
      return False
  for ru in rejected_users:
    if ru in user:
      return False
  return True

def load_data():
  global filtered_tweets
  global last_id
  tweets_file = open(TWEETS_PICKLE_FILE,'rb')
  filtered_tweets = pickle.load(tweets_file)

def save_data():
  tweets_file = open(TWEETS_PICKLE_FILE,'wb')
  pickle.dump(filtered_tweets, tweets_file)

api = twitter.Api(
    consumer_key = mv_consumer_key,
    consumer_secret = mv_consumer_secret,
    access_token_key = mv_access_token,
    access_token_secret = mv_access_token_secret
)

keywords_set = [
  ['#DonaTusMedicinas'],
  ['#ServicioPublico']
]

users = [
  'donatumed',
  'ayudamedicinasv'
]

unfiltered_tweets = []
filtered_tweets = {}

for u in users:
  unfiltered_tweets += api.GetUserTimeline(screen_name=u, count=5000)

for ks in keywords_set:
  for word in ks:
    unfiltered_tweets += api.GetSearch(term=word, count=5000)

load_data()

new_tweets = 0

for tw in unfiltered_tweets:
  tw_hash = hashlib.md5(tw.text.encode('utf8')).hexdigest()
  if tw_hash not in filtered_tweets:
    if apply_filters(tw):
      filtered_tweets[tw_hash] = tw.AsDict()
      new_tweets += 1

save_data()

print 'Found {0} new tweets! Current size is: {1}'.format(new_tweets, len(filtered_tweets))