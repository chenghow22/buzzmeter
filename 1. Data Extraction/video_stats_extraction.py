# Setup and import library
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
youTubeApiKey = "yourAPIkey"
youtube = build("youtube","v3",developerKey = youTubeApiKey)

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
'https://www.youtube.com/watch?v=videoid'
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
            'videoid' : video_id,
            'videoname': video_snippet.get('title', ''),
            'views': video_statistics.get('viewCount', 0),
            'likes': video_statistics.get('likeCount', 0),
            'comments': video_statistics.get('commentCount', 0),
            'publishdate': video_snippet.get('publishedAt', '')
        }
    else:
        print(f"Unable to retrieve video data for URL: {url}")

# Print the total number of video data retrieved
total_data_retrieved = len(video_data_dict)
print(f"Total number of video data retrieved: {total_data_retrieved}")

# Convert video_data_dict into a DataFrame
df = pd.DataFrame.from_dict(video_data_dict, orient='index')

# Reset the index of dataframe
df = df.reset_index(drop=True)

# Convert the data type before loading into BigQuery 
df.views = df.views.astype(int)
df.likes = df.likes.astype(int)
df.comments = df.comments.astype(int)

# TODO: Set project_id to your Google Cloud Platform project ID.
project_id = 'project-id'

# TODO: Set table_id to the full destination table ID (including the dataset ID).
destination_table = 'project-id.dataset.table1'

pandas_gbq.to_gbq(df,
                  destination_table,
                  project_id=project_id,
                  chunksize=None, # I have tried with several chunk sizes, it runs faster when it's one big chunk (at least for me)
                  if_exists='replace', # Use the if_exists argument to dictate whether to 'fail', 'replace' or 'append' if the destination table already exists. The default value is 'fail'.
                  table_schema=[{'name': 'videoid','type': 'STRING'},
                               {'name': 'videoname','type': 'STRING'},
                               {'name': 'views','type': 'INTEGER'},
                               {'name': 'likes','type': 'INTEGER'},
                               {'name': 'comments','type': 'INTEGER'},
                               {'name': 'publishdate','type': 'STRING'}],
                  verbose=False
                  )