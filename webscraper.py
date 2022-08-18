import snscrape.modules.twitter as sntwitter
import pandas as pd


def get_tweets_from_user(username):
    # Created a list to append all tweet attributes(data)
    attributes_container = []

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{username}').get_items()):
        if i > 100:
            break
        attributes_container.append([tweet.date, tweet.likeCount, tweet.sourceLabel, tweet.content])

    # a new dataframe gets created and filled with the attributes_container
    # tweets_df = pd.DataFrame(attributes_container, columns=["Date Created", "Number of Likes", "Source of Tweet", "Tweets"])

    # the tweets_df is then returned
    return attributes_container


def get_tweets_from_search_with_date(search_string, start_time, end_time):
    # Created a list to append all tweet attributes(data)
    attributes_container = []

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{search_string} + since:{start_time} until:{end_time}').get_items()):
        if i > 100:
            break
        attributes_container.append([tweet.date, tweet.likeCount, tweet.sourceLabel, tweet.content])

    # a new dataframe gets created and filled with the attributes_container
    # tweets_df = pd.DataFrame(attributes_container,
    #                          columns=["Date Created", "Number of Likes", "Source of Tweet", "Tweets"])

    # the tweets_df is then returned
    return attributes_container

# tests to see if the functions work
# print(get_tweets_from_user("fabbo_23"))
# print(get_tweets_from_search_with_date('its the elephant', '2020-06-01', '2020-07-31'))
