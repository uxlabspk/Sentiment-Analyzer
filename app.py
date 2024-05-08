from flask import Flask, request, render_template
from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/comments', methods=['POST', 'GET'])
def comments():
    error_string = ""
    if request.method == 'POST' and 'video_id' in request.form:
        video_id = request.form['video_id']
        api_key = "AIzaSyCbVl5WF2TXBwN6RppZQe7-Trao38R2rEs"
        youtube = build('youtube', 'v3', developerKey=api_key)
        comments = youtube.commentThreads().list(
            part = "snippet",
            videoId = video_id,
            maxResults = 100
        ).execute()
        # Initilizatoin
        analyzer = SentimentIntensityAnalyzer()
        # Perform sentiment analysis on each comment
        for comment in comments['items']:
            text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
            sentiment_score = analyzer.polarity_scores(text)
            comment['sentiment'] = sentiment_score
            
        return render_template('comments.html', comments = comments['items'])

    else:
        error_string = "error occur"
        return render_template('index.html', error_code = error_string)

    return "sdf"




if __name__ == '__main__':
    app.run(debug=True)
