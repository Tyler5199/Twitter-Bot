# import modules
import tweepy
import requests
import time
import json


# Create Constants for API Access Keys
CONSUMER_KEY = 'vTgu16GU0qFpsJU1R9Wfnscco'
CONSUMER_SECRET = '0LYfdA8YN1dQlGrQWiNYO6ZC7oayfQ3DXCrBxaYCMTOc4t7zAX'
ACCESS_KEY = '1147722889770295296-LtOPtL1DlQ7sFtnLhpV7KdgCjYQ1vX'
ACCESS_SECRET = '7p4Bo3RGfBFyhFotWjwhuUjDRdS6tP8IRxcTFtoE8tmlH'
WEATHER_KEY = '6928e77c53654089a75ac46db53282b5'


# Connect to twitter API using tweepy
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
twitter_api = tweepy.API(auth)


# Create Constants referencing text file names to store tweet IDs


# File used to store the tweet ID for the last seen Donald Trump tweet
TRUMP_FILE_NAME = 'trump_last_seen_id.txt'

# File used to store the tweet ID for the last seen account mention
LAST_MENTION_FILE_NAME = 'mentions_last_seen_id.txt'

# Create a constant accessing Donald Trumps twitter account
DONALD = twitter_api.get_user("@realDonaldTrump")


# Retrieves the last tweet ID from the TRUMP text file
def retrieve_trump_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    trump_last_seen_id = int(f_read.read().strip())
    f_read.close()
    return trump_last_seen_id


# Stores the last tweet ID into the trump_last_seen_id.txt file
def store_trump_last_seen_id (trump_last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(trump_last_seen_id))
    f_write.close()
    return


# Replies to all of Donald Trump's tweets with an ID number greater than the one stored
    # in the trump_last_seen_id.txt file
def reply_to_tweets():

    print('retrieving and replying to Tweets...')


# Stores the last 20 tweets from Donald Trump's timeline into a list named tweets
    tweets = twitter_api.user_timeline(DONALD.screen_name)


# Cycles through tweets and checks to see if tweet id of each tweet is greater than the one stored
    # in the trump_last_seen_id.txt file
    for status in tweets:
        trump_last_seen_id = retrieve_trump_last_seen_id(TRUMP_FILE_NAME)

        if status.id > trump_last_seen_id:

            # Stores the newest tweet ID into the trump_last_seen_id.txt file
            store_trump_last_seen_id(status.id, TRUMP_FILE_NAME)
            print("Replying to Trump...")

            # Replies to each of Trump's specified by the ID od each status
            twitter_api.update_status("@" + DONALD.screen_name + " Hey! Climate change is real!", status.id)


# Returns the last stored tweet ID from the mentions_last_seen_id.txt file
def retrieve_mentions_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    mentions_last_seen_id = int(f_read.read().strip())
    f_read.close()
    return mentions_last_seen_id


# Stores a tweet ID in the mentions_last_seen_id.txt file
def store_mentions_last_seen_id(mentions_last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(mentions_last_seen_id))
    f_write.close()
    return


# Returns a list of cities, a list of screen_names, and a list of ids from tweets mentioning the account
def get_data():

    # Retrieves the last seen ID from the mentions_last_seen_id.txt file
    mentions_last_seen_id = retrieve_mentions_last_seen_id(LAST_MENTION_FILE_NAME)

    # Stores all of the account mentions after the last seen mention into a list
    mentions = twitter_api.mentions_timeline(mentions_last_seen_id, tweet_mode ='extend')

    # Creates lists to store data from the mentioned tweets
    city = []
    screen_names = []
    ids = []

    # Cycles through list of mentions and adds the data located in each mention to the corresponding lists
    for mention in reversed(mentions):
        city.append(mention.text.strip("@robotsVSrays "))
        screen_names.append(mention.user.screen_name)
        ids.append(mention.id)

        # Stores the ID of the mention into the mentions_last_seen_id.txt file
        mentions_last_seen_id = mention.id
        store_mentions_last_seen_id(mentions_last_seen_id, LAST_MENTION_FILE_NAME)

    return city, screen_names,ids


# Gathers weather data from weatherbit.com and replies to tweet
def reply_weather_reports():

    # Establish variables to hold data from tweet
    data = get_data()
    cities = data[0]
    screen_names = data[1]
    ids = data[2]

# Access Weather API and check access code
    for i in range(len(cities)):
        print(cities[i])
        print(screen_names[i])
        print(ids[i])
        weather_city_url = 'https://api.weatherbit.io/v2.0/current?city=' + cities[i] + '&units=I&key=' + WEATHER_KEY
        data = requests.get(weather_city_url)
        status_code = data.status_code

        # If weather data is successfully accessed add data to an array
        if status_code == 200:

            content = data.content
            content_array = json.loads(content)

            # Store each aspect of weather data into corresponding variables
            for x in content_array['data']:
                temp = x['temp']
                weather = (x['weather'])
                weather_description = weather['description']
                wind_speed = x['wind_spd']
                precipitation = x['precip']
                snow = x['snow']
                humidity = x['rh']

            # Reply to twitter status with weather data
            twitter_api.update_status("@" + screen_names[i] + "\n" + cities[i] + "\nTemperature: " + str(temp) + "° F" +
                                      "\nWeather: " + weather_description + "\nHumidity: " + str(humidity) +
                                      "\nAmount of Precipitation: " + str(precipitation) + " in" + "\nWind Speed: " + str(wind_speed) + " mph", ids[i])

        # If weather data is not correctly accessed reply to the tweets with an error message
        if status_code == 204:
            twitter_api.update_status("@" + screen_names[i] + ' Your tweet was not formatted correctly.'
                                                              ' Please reformat and try again!'
                                                              '\n\nP.S. The correct format is in our bio', ids[i])


# Check every 15 seconds to see if account in mentioned in a tweet if it is respond to the tweet
while True:
    reply_to_tweets()
    reply_weather_reports()
    time.sleep(15)

