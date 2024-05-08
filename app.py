from flask import Flask, request, render_template
from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv
import os
import re

load_dotenv()
api_KEY = os.getenv('API_KEY')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/comments', methods=['POST', 'GET'])
def comments():
    error_string = ""
    if request.method == 'POST' and 'video_id' in request.form:
        video_id = get_youtube_video_id(request.form['video_id'])
        api_key = api_KEY
        youtube = build('youtube', 'v3', developerKey=api_key)
        comments = youtube.commentThreads().list(
            part = "snippet",
            videoId = video_id,
            maxResults = 100
        ).execute()

        analyzer = SentimentIntensityAnalyzer()

        for comment in comments['items']:
            text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
            sentiment_score = analyzer.polarity_scores(text)
            comment['sentiment'] = sentiment_score
            
        return render_template('comments.html', comments = comments['items'])

    else:
        error_string = "error occur"
        return render_template('index.html', error_code = error_string)

    return "sdf"



def get_youtube_video_id(url):
    pattern = r"^https:\/\/(?:www\.|m\.)?youtube\.com\/(?:watch\?v=|embed\/|v\/|shorts\/|)([^#\&\?]*).*"
    match = re.match(pattern, url)
    if match:
        return match.group(1)
    else:
        return "Invalid url"




if __name__ == '__main__':
    app.run(debug=True)
