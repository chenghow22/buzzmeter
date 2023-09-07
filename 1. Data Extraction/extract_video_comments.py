#import library
from googleapiclient.discovery import build
import pandas as pd
import plotly.express as px
import urllib.parse as p
from datetime import datetime, timedelta
import pytz
import pandas_gbq
import re

# youtube api key
# replace with your API key
youTubeApiKey = "YOUR_YOUTUBE_API_KEY"
youtube = build("youtube","v3",developerKey = youTubeApiKey)

#function to retrieve comment from a youtube video
def get_comments(youtube, **kwargs):
    return youtube.commentThreads().list(
        part="snippet",
        **kwargs
    ).execute()

#function to retrieve video id from video url
def get_video_id_by_url(url):
    if "watch" in url:
        video_id_pattern = re.compile(r'v=(.{11})')
        video_id = video_id_pattern.findall(url)
        if video_id:
            return video_id[0]
    elif "shorts" in url:
        video_id_pattern = re.compile(r'shorts/(.{11})')
        video_id = video_id_pattern.findall(url)
        if video_id:
            return video_id[0]
    return None

# Input the list of video urls
urls = [
"https://www.youtube.com/watch?v=videoid"
]
print(f"Number of video input: {len(urls)}")

# Initialize a dictionary to store video data for each URL
video_data_dict = {}

# Retrieve video data including name, statistics, and publish date for each URL
for url in urls:
    video_id = get_video_id_by_url(url)
    if video_id:
        response = youtube.videos().list(
            part='snippet,statistics',  # Include snippet and statistics
            id=video_id
        ).execute()
        # Extract video snippet and statistics
        video_snippet = response['items'][0]['snippet']
        video_statistics = response['items'][0]['statistics']
        video_data_dict[url] = {
            'VideoName': video_snippet.get('title', ''),
            'Views': video_statistics.get('viewCount', 0),
            'Likes': video_statistics.get('likeCount', 0),
            'Comments': video_statistics.get('commentCount', 0),
            'PublishDate': video_snippet.get('publishedAt', '')
        }
    else:
        print(f"Unable to retrieve video data for URL: {url}")

# Print the total number of video data retrieved
total_data_retrieved = len(video_data_dict)
print(f"Total number of video data retrieved: {total_data_retrieved}")

# Initialize lists to store comments and other attributes
id_conso = []
comment_conso = []
updated_conso = []
like_conso = []
comment_id_conso = []

# Define the number of pages to retrieve
n_pages = 30  # Adjust as needed

# Iterate through the video URLs
for url in urls:
    # Get the video ID from the URL
    video_id = get_video_id_by_url(url)
    if video_id:
        # Initialize parameters for comment retrieval for this video
        params = {
            'videoId': video_id,
            'maxResults': 300,  # Adjust the number of results per page as needed
            'order': 'relevance',  # Default is 'time' (newest)
        }

        # Initialize a flag for pagination
        next_page_token = None

        # Initialize a page counter
        page_count = 0

        while page_count < n_pages:
            try:
                # Fetch comments for a specific video and page
                response = get_comments(youtube, **params)
                items = response.get("items")

                if not items:
                    break

                for item in items:
                    video_id = item["snippet"]["videoId"]
                    comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                    updated_at = item["snippet"]["topLevelComment"]["snippet"]["updatedAt"]
                    like_count = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
                    comment_id = item["snippet"]["topLevelComment"]["id"]

                    id_conso.append(video_id)
                    comment_conso.append(comment)
                    updated_conso.append(updated_at)
                    like_conso.append(like_count)
                    comment_id_conso.append(comment_id)

                # Check if there is a next page
                if "nextPageToken" in response:
                    params["pageToken"] = response["nextPageToken"]
                else:
                    break

                # Increment the page counter
                page_count += 1

            except Exception as e:
                print(f'Error fetching comments for video URL: {url}')
                print(f'Error message: {str(e)}')

# Print the total number of comments extracted
print(f'Total number of comments extracted: {len(comment_conso)}')

data = {'date':updated_conso,'video_id':id_conso,'comment':comment_conso,'like_count':like_conso,'comment_id':comment_id_conso}
df = pd.DataFrame(data)
df