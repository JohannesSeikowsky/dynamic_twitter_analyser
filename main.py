""" 
Dynamic Twitter Analyser
Allows one to analyse what time intervals may be best to tweet in.

Example: 
main("AldiUK", 200, 30)

Retrieves the last 200 Tweets of AldiUK, divides the day into intervals
of 30 minutes (0.00-0.30, 0.30-1.00, 1.00-1.30 etc) then calculates
the average popularity of the tweets in each interval (in terms of likes and retweets) .
Finally plots the results in a graph, hopefully clarifying which time
intervals have a good chance to see popular tweets.
"""	

import GetOldTweets3 as got
import datetime
import matplotlib.pyplot as plt
import random


# Settings
retweet_weighing = 1.4 # how many likes a retweet is worth in terms of "popularity score"


def get_tweets(target_account, tweet_volume):
	""" get certain amount of tweets from a particular twitter account """
	tweetCriteria = got.manager.TweetCriteria().setUsername(target_account).setTopTweets(True).setMaxTweets(tweet_volume)
	tweets = got.manager.TweetManager.getTweets(tweetCriteria)
	return tweets


def add_minutes_to_time(time, minutes_to_add):
	""" take in a time object and add certain number of minutes to that time """
	time_delta = datetime.timedelta(minutes=minutes_to_add)
	time_as_datetime = datetime.datetime.combine(datetime.date(1, 1, 1), time)
	new_time = (time_as_datetime + time_delta).time()
	return new_time


def generate_intervals(interval_length):
	""" chuck up day into intervals of a certain length """
	minutes_per_day = 24*60
	number_of_intervals = int(minutes_per_day / interval_length)

	# generate start-times of all intervals
	times = []
	time = datetime.time()
	for _ in range(number_of_intervals):
		times.append(time)
		time = add_minutes_to_time(time, interval_length)

	# join all start-times with their corresponding end-times
	intervals = []
	for each in range(len(times)-1):
		intervals.append([times[each], times[each+1]])
	return intervals


def generate_barplot(target_account, analysis_interval, x_values, y_values):
	""" generate and save a barplot """
	plt.bar(x_values, y_values)
	file_name = target_account.lower() + "-" + str(analysis_interval)
	plt.savefig(file_name)




def main(target_account, tweet_volumne, analysis_interval):
	""" retrivee tweets, calculate average tweet popularity for each interval, plot results """
	tweets = get_tweets(target_account, tweet_volumne)
	intervals = generate_intervals(analysis_interval)

	# dicts for recording total tweet count and 
	# total popularity of all tweets for each interval
	tweet_counts, popularity_counts = {}, {}
	for each in intervals:
		start_time = str(each[0])
		tweet_counts[start_time] = 0
		popularity_counts[start_time] = 0

	# count number of tweets and total popularity for each interval 
	for tweet in tweets:
		for interval_start, interval_finish in intervals:
			if interval_start < tweet.date.time() < interval_finish:
				# increment tweet count of interval
				interval_key = str(interval_start)
				tweet_counts[interval_key] = tweet_counts[interval_key] + 1
				# raising total popularity count of interval
				tweet_popularity = tweet.favorites + retweet_weighing * tweet.retweets 				
				popularity_counts[interval_key] = popularity_counts[interval_key] + tweet_popularity
				break

	# calculate average tweet popularity for each interval
	interval_popularities = {}
	for each in tweet_counts.keys():
		tweet_count = tweet_counts[each]
		popularity_count = popularity_counts[each]
		if tweet_count > 0:
			interval_popularities[each] = round(popularity_count / tweet_count, 1)
		else:
			interval_popularities[each] = 0

	# plotting average tweet popularity
	x_values = interval_popularities.keys()
	y_values = interval_popularities.values()
	generate_barplot(target_account, analysis_interval, x_values, y_values)
