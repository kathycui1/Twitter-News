import tweepy
from newsapi import NewsApiClient
import datetime, time

api_news_key = '4f56344553134c8d8b8e11fd46fca307'
newsapi = NewsApiClient(api_key=api_news_key)
top_headlines = newsapi.get_top_headlines(language='en',
										country='ca')
articles = top_headlines['articles']
api_key = 'Z5KFVXPqzakGbKVSMlqtRTIYx'
api_secret = 'j32OIq9AgrLaz26gI2wWWGYtpk4Ej9Pz481zNTTfnFbXQUAdm7'
access_token = '1388990186764357643-gxDUtr29IihfZqIm0YLPrL1GlFVn2E'
access_token_secret = 'lpUaLrjeU1Oc08QOXnsrhWByUAH4X4RjCa5ukHPqjUSPZ'
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Retrieves the top news headlines from News API and returns a list of them
def newsheadlines():
	sources = []
	for x, y in enumerate(articles):
		sources.append(f'{x} {y["title"]}')
	return sources

# Takes the list of the top news headlines and returns a list of correctly
# formatted headlines for a Twitter post
def tweetheadlines():
	tweet_sources = []
	news_headlines = newsheadlines()
	for headline in news_headlines:
		first_space = headline.find(' ')
		updated_headline = headline[first_space:]
		tweet_sources.append(updated_headline)
	return tweet_sources

# Retrieves the top news URLs from News API and returns a list of them
def urlheadlines():
	url_links = []
	for x, y in enumerate(articles):
		url_links.append(f'{x} {y["url"]}')
	return url_links

# Obtains the list of the top news URLs and returns a list of correctly
# formatted URLs for a Twitter post
def tweeturl():
	url_links_lst = []
	url_links = urlheadlines()
	for link in url_links:
		first_space = link.find(' ')
		updated_link = link[first_space:]
		url_links_lst.append(updated_link)
	return url_links_lst

# Retrieves the 200 most recent tweets from the user and returns a list of 
# the tweets' texts
def old():
	timeline = api.user_timeline(user_id='NewsAlertsCA', count=200, tweet_mode="extended")
	text = [tweet.full_text for tweet in timeline]
	return text
old_lst = old()

# Combines the corresponding top news headlines and URLs and returns them
# as a list where they are correctly formatted for a Twitter post
def tweets():
	index = 0
	lst_tweets = []
	headlines = tweetheadlines()
	url_links = tweeturl()
	for headline in headlines:
		tweet_text = []
		headline = headlines[index]
		url = url_links[index]
		tweet_text.append(headline)
		tweet_text.append(url)
		index += 1
		final_tweet = tweet_text[0] + ' ' + tweet_text[1]
		lst_tweets.append(final_tweet)
	updated_lst_tweets = []
	for tweet in lst_tweets:
		first_space = tweet.find(' ')
		updated_tweet = tweet[first_space + 1:]
		updated_lst_tweets.append(updated_tweet)
	return updated_lst_tweets

# Compares the 200 most recent tweets from old() with the new list 
# of tweets from tweets() and removes any duplicates from the new list
def removeduplicates(old_lst_tweets, new_lst_tweets):
	index = 0
	duplicates = []
	combined = '\t'.join(old_lst_tweets)
	for tweet in new_lst_tweets:
		if new_lst_tweets[index][0:10] in combined:
			duplicates.append(tweet)
		index += 1
	for dup in duplicates:
		if dup in new_lst_tweets:
			new_lst_tweets.remove(dup)
	return new_lst_tweets

# Posts the new list of tweets from removeduplicates() to the Twitter
# account using tweepy every 3 hours
def posttweet(old_lst):
	old_lst = old()
	new_lst = tweets()
	lst_no_dupes_tweets = removeduplicates(old_lst, new_lst)
	old_lst = new_lst
	if len(lst_no_dupes_tweets) > 0:
		for tweet in lst_no_dupes_tweets:
			api.update_status(tweet)
	else:
		print('empty')
	time.sleep(10800)

while True:
	posttweet(old_lst)