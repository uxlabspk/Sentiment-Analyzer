from flask import Flask, request, render_template
from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv
import os
import re
import html

load_dotenv()
api_KEY = os.getenv('API_KEY')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/comments', methods=['POST', 'GET'])
def comments():
    if request.method == 'POST' and 'video_id' in request.form:
        if (request.form['video_id'].startswith("@")):
            channel = get_youtube_channel_name(request.form['video_id'])
            api_key = api_KEY
            return fetchChannelVideos(channel, api_key)        

        video_id = get_youtube_video_id(request.form['video_id'])
        api_key = api_KEY
        return fetchComments(video_id, api_key)    

    return render_template('index.html')



def get_youtube_channel_name(url):
    return url[1:]  


def get_youtube_video_id(url):
    pattern = r"^https:\/\/(?:www\.|m\.)?youtube\.com\/(?:watch\?v=|embed\/|v\/|shorts\/|)([^#\&\?]*).*"
    match = re.match(pattern, url)
    if match:
        return match.group(1)
    else:
        return -1


def fetchChannelVideos(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # Call the channels.list method to retrieve information about the channel
    # channels_response = youtube.channels().list(
    #     part='contentDetails',
    #     forUsername=video_id
    # ).execute()

    channels_response = youtube.search().list(
        part='snippet'
    ).execute()
    
    # Get the channel ID
    # channel_id = channels_response['etag']
    # # channel_id = channels_response['items'][0]['id']
    
    # # # Call the playlistItems.list method to retrieve the most recent videos from the channel
    # playlist_items_response = youtube.playlistItems().list(
    #     part='snippet',
    #     playlistId=channel_id,
    #     maxResults=10
    # ).execute()

    # print(playlist_items_response)
    
    # # Extract video information
    # videos = []
    # for item in playlist_items_response['items']:
    #     videos.append({
    #         'title': item['snippet']['title'],
    #         'video_id': item['snippet']['resourceId']['videoId']
    #     })
    
    return render_template('channelVideos.html', response=channels_response)
    # return render_template('404.html')



def fetchComments(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
        
    try:
        comments = youtube.commentThreads().list(
            part = "snippet",
            videoId = video_id,
            maxResults = 100
        ).execute()
    except:
        print("Something went wrong")
        return render_template('404.html')

    analyzer = SentimentIntensityAnalyzer()

    positive_Average = 0
    negative_Average = 0
    filtered_comments = []

    for comment in comments['items']:
        text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
        comment['snippet']['topLevelComment']['snippet']['textDisplay'] = re.sub(r'<.*?>', '', comment['snippet']['topLevelComment']['snippet']['textDisplay'])
        sentiment_score = analyzer.polarity_scores(text)
        comment['sentiment'] = sentiment_score

        
        positive_Average += comment['sentiment']['pos']
        negative_Average += comment['sentiment']['neg']

        words = text.split(" ")
        found_keywords = []
        for word in words:
            if word in ['audio', 'video', 'recommendation', 'song']:
                found_keywords.append(word)
        if found_keywords:
            comment['found_keywords'] = found_keywords
            filtered_comments.append(comment)     

    return render_template('comments.html', comments = comments['items'], avg_positive = round(positive_Average) / 100, avg_negative = round(negative_Average) / 100, filteredComment=filtered_comments)



if __name__ == '__main__':
    app.run(debug=True)
