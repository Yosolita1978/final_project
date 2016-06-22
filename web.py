from flask import Flask, render_template, request, redirect, flash
import security_info
import json
import final_project
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/search/', methods=["GET", "POST"])
def search():
    error = ""
    my_tweets = []
    hashtag = ""
    if request.method == "POST":
        hashtag = request.form["hashtag"]
        if hashtag == "":
            error = "Please search for a #Hashtag first"            
        else:      
            my_tweets = final_project.search_hashtag(hashtag)
            tweet_list = json.dumps(my_tweets)
            with open('/Users/cristina/Source/final_project/tweet_list.txt',"w") as my_file:
                my_file.write(tweet_list)
    
    return render_template('search.html', hashtag=hashtag, tweets=my_tweets, error=error)

def read_tweets():
    with open('/Users/cristina/Source/final_project/tweet_list.txt') as my_file:
        my_tweets = json.loads(my_file.read())
    return my_tweets

def find_tweet(list_tweets, id_tweet):
    for tweet in list_tweets:
        if tweet["id_str"] == id_tweet:
            return tweet
        

@app.route('/follow/', methods=["GET", "POST"])
def follow():    
    my_tweets = read_tweets()
    if request.method == "GET":
        id_tweet = request.args["id"]
        tweet = find_tweet(my_tweets, id_tweet)
        return render_template('follow.html', tweet=tweet)
    else:
        id_tweet = request.form["id"]
        tweet = find_tweet(my_tweets, id_tweet)
        twitter_session = final_project.get_twitter_session()
        message = final_project.follow_user(twitter_session,tweet)
        flash(message)
        return redirect("/")

@app.route('/send/', methods=["GET", "POST"])
def send():
    my_tweets = read_tweets()
    if request.method == "GET":
        id_tweet = request.args["id"]
        tweet = find_tweet(my_tweets, id_tweet)
        return render_template('send.html', tweet=tweet)
    else:
        id_tweet = request.form["id"]
        tweet = find_tweet(my_tweets,id_tweet)
        twitter_session = final_project.get_twitter_session()
        message = request.form["message"]
        success = final_project.post_tweet(twitter_session, tweet, message)
        flash(success)
        return redirect("/")

    

if __name__ == "__main__":
    app.secret_key = security_info.APP_SECRET_KEY
    app.run(debug=True)