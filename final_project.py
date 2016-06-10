# encoding: utf-8
from security_info import *
import subprocess
import requests 
from requests_oauthlib import OAuth1, OAuth1Session
import os.path

URL = "https://api.twitter.com/1.1/search/tweets.json"
API_KEY = TWITTER_API_KEY 
API_SECRET = TWITTER_API_SECRET
my_tweets = []

def tweet_string(tweet):
    return "* %s, %s, %s : %s \n" %(tweet["id_str"], tweet["user"]["name"],tweet["user"]["screen_name"], tweet["text"])  

def search_hashtag():
    global my_tweets
    auth = OAuth1(API_KEY, API_SECRET)
    hashtag = raw_input("Please type the #hashtag that you want to search: ")
    params = {"q": hashtag, "count": 20, "lang":"en"}
    response = requests.get(URL, params=params, auth=auth)
    search_results = response.json()
    my_tweets = search_results["statuses"]
    for tweet in my_tweets:
        print tweet_string(tweet)

def your_messages():
    user_message1 = "Hello! We are excited to introduce @Tejiendo_MiVida Crochet, very soon an online store for handmade crochet"
    user_message2 = "HI, just saw that you love to crochet so I wanted to introduce you to my work in @Tejiendo_MiVida"
    user_message3 = "Hi! Amazing work!. After seeing your work, I will never look at a crochet in the same way!"
    user_message = raw_input("""
    This are your messages:

    1. %s

    2. %s

    3. %s
     """ %(user_message1, user_message2, user_message3))
    if user_message == "1":
        return user_message1
    elif user_message == "2":
        return user_message2
    elif user_message == "3":
        return user_message3
    else:
        return raw_input("Please type the message of your tweet. Remember not more that 140 caracters ")


def post_tweet(twitter, tweet):
    message = your_messages()
    username = "@%s" %(tweet["user"]["screen_name"])
    status = ("%s %s") %(username, message)
    in_replay_to_status_id = tweet["id_str"]
    params = {"status": status, "in_replay_to_status_id": in_replay_to_status_id}
    response = twitter.post("https://api.twitter.com/1.1/statuses/update.json", params)
    print "You send the tweet: %s" %(status)

def follow_user(twitter, tweet):
    username = "@%s" %(tweet["user"]["screen_name"])
    params = {"screen_name": username}
    response = twitter.post("https://api.twitter.com/1.1/friendships/create.json", params)
    print "Now you are following %s" %(username)


def write_list():
    global my_tweets
    with open('/Users/cristina/Source/final_project/tuits_list.txt',"w") as my_file:
        for tweet in my_tweets:
            my_file.write(tweet_string(tweet).encode("utf-8"))

def read_list():
    with open('/Users/cristina/Source/final_project/tuits_list.txt') as my_file:
        for line in my_file:
            print line.strip()

def show_menu():
    user_choice = raw_input("""
        This is your Twitter Robot. What do you want to do:
            1. Search for a Hashtag
            2. Follow an user
            3. Send a tweet to a user
            4. Write your tweets in a .txt
            5. Read your .txt """)
    return user_choice


def main():
    global my_tweets
    twitter = OAuth1Session(API_KEY, client_secret=API_SECRET, resource_owner_key=TWITTER_ACCESS_TOKEN, resource_owner_secret=TWITTER_TOKEN_SECRET)

    while True:

        user_choice = show_menu()

        if user_choice == "1":
            search_hashtag()

        elif user_choice == "2":
            if len(my_tweets) == 0:
                print "Please search for a hashtag first. You only can send a tweet from your search"
            else:
                index_tweet = -1
                while index_tweet < 0 or index_tweet > len(my_tweets) - 1:
                    index_tweet = int(raw_input("Please select a user from your list of tweets. Choose from 0 - %s: " %(len(my_tweets)-1)))
                tweet = tweet_string(my_tweets[index_tweet])
                confirmation = raw_input(u"You are gonna follow to %s. Are you sure: Y or N: " %(tweet.decode("utf-8")))
                if confirmation.upper() == "Y":
                    follow_user(twitter, my_tweets[index_tweet])
                else:
                    pass
            

        elif user_choice == "3":
            if len(my_tweets) == 0:
                print "Please search for a hashtag first. You only can send a tweet from your search"
            else:
                index_tweet = -1
                while index_tweet < 0 or index_tweet > len(my_tweets) - 1:
                    index_tweet = int(raw_input("Please select a tweet to replay from your list. Choose from 0 - %s: " %(len(my_tweets)-1)))
                tweet = tweet_string(my_tweets[index_tweet])
                confirmation = raw_input(u"You are gonna send a tweet to %s. Are you sure: Y or N: " %(tweet.decode("utf-8")))
                if confirmation.upper() == "Y":
                    post_tweet(twitter, my_tweets[index_tweet])
                else:
                    pass
            
        
        elif user_choice == "4":
            if len(my_tweets) == 0:
                print "Please search for a hashtag first. You only can save tweets from your search list"
            else:
                write_list()

        elif user_choice == "5":
            if os.path.isfile('/Users/cristina/Source/final_project/tuits_list.txt') is False:
                print "You dont have a file with tweets to show"
            else:
                read_list()
            

        else:
            break




if __name__ == '__main__':
    main()
#