# twitter-extractor 

An extraction tool for  building machine learning training sets from Twitter.

## Set up ##

#### Install python 2.7 ####
* Ubuntu/Debian:
```sudo apt-get install python2.7```
* Fedora:
```sudo yum install python2.7```
* Arch:
```sudo pacman -S python2```

#### Install pip through package manager ####
* Ubuntu/Debian:
```sudo apt-get install python-pip```
* Fedora:
```sudo yum install python-pip```
* Arch:
```sudo pacman -S python2-pip```

#### Python dependencies ####
* twitter
```pip install twitter```

## Specifications file ##

To get the extractor running you only need to fill the spec_information.py file. First you will need to create a twitter app [here](https://apps.twitter.com/), 
and then go to ** Keys and Access Tokens ** to get your consumer key and access token, you will need this information
to access twitter.

~~~~~
spec_consumer_key = '...'
spec_consumer_secret = '...'
spec_access_token = '...'
spec_access_token_secret = '...'
~~~~~

In the examples folder you will find an example of how the configuration file must look.
Minimal required information is either some keyword or twitter user to produce a search. Keywords are created as lists, in order to provide searches using multiple words in future versions. If you just want one of these then ** define both ** but leave the other in blank.
~~~~~
spec_keywords = [
  ['#...'],
  ...
]

spec_users = [
  '...',
  ...
]
~~~~~

If you like you can also specify rejected users and keywords.
~~~~~
spec_rejected_keywords = ['...']
spec_rejected_users = ['...']
~~~~~

## Usage ##

The extractor works like this: first performe a search to get tweets from the Twitter API, apply filters if defined in
spec file, remove exact dupplicates and then store them in a python pickle. A pickle is a way add persistency to a python object and they will be stored in a pickles folder generated on the first search.

To look for tweets do:
~~~~~
./find_tweets.py
~~~~~

You can run this as many times as you want. Whenever you want to export the existing tweets to a csv file do:
~~~~~
./get_tweets.py
~~~~~

This will create a csv file in the csv folder with the new tweets found after the last export. If you loose this csv file or if you want to get all the existing tweets from start just erase the file ```pickles/exported_tweets.p``` and run find_tweets again.

For the moment the only way to get full information of the tweets collected (date, retweet count, user, and such) is to load the pickle file ```pickles/filtered_tweets.p```.

## Future Work ##


## Author ##

**Simon Bolivar University**, 2014. Sofia Bravo. 09-10114@usb.ve.
