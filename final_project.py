from security_info import TWITTER_API_KEY, TWITTER_API_SECRET
import subprocess
import requests 
from requests_oauthlib import OAuth1
import os.path

URL = "https://api.twitter.com/1.1/search/tweets.json"
API_KEY = TWITTER_API_KEY
API_SECRET = TWITTER_API_SECRET
my_tweets = []

def tweet_string(tweet):
        return "* %s : %s \n" %(tweet["user"]["name"], tweet["text"]) 

def search_hashtag():
    global my_tweets
    auth = OAuth1(API_KEY, API_SECRET)
    hashtag = raw_input("Please type the #hashtag that you want to search: ")
    params = {"q": hashtag, "count": 20, "lang":"en"}
    response = requests.get(URL, params=params, auth=auth)
    search_results = response.json()
    my_tweets = search_results["statuses"]
    for tweet in my_tweets:
        #print tweet
        print tweet_string(tweet)


def write_list():
    global my_tweets
    with open('/Users/cristina/Source/final_project/tuits_list.txt',"w") as my_file:
        for tweet in my_tweets:
            my_file.write(tweet_string(tweet).encode("utf-8"))

def read_list():
    with open('/Users/cristina/Source/final_project/tuits_list.txt') as my_file:
        for line in my_file:
            print line.strip()


def main():
    user_choice = raw_input("""
                            This is your Twitter Robot. What do you want to do:
                            1. Search for a Hashtag
                            2. Read your tweets in .txt
                            3. Follow an user
                            4. Send a tweet to an user  """)

    if user_choice == "1":
        search_hashtag()
        write_list()
    if user_choice == "2":
        if os.path.isfile('/Users/cristina/Source/final_project/tuits_list.txt') is False:
            print "You dont haver a file with tweets to show"
        else:
            read_list()
    else:
        pass


if __name__ == '__main__':
    main()
#