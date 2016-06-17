from flask import Flask, render_template, request
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

if __name__ == "__main__":
    app.run(debug=True)