# Setup and import library
from googleapiclient.discovery import build
import pandas as pd

# Setup your youtube api key
youTubeApiKey = "yourAPIkey"
youtube = build("youtube","v3",developerKey = youTubeApiKey)

# Input the channel name
channelUsername= "jxbdlut"

# Channel stats
channelStats = youtube.channels().list(part = "snippet,contentDetails,statistics", forUsername=channelUsername).execute()
channelStatistics = channelStats["items"][0]["statistics"]
channelStatistics

# Get the Subscriber counts, video counts, and view counts
subscriberCount = channelStatistics["subscriberCount"]
videoCount = channelStatistics["videoCount"]
viewCount = channelStatistics["viewCount"]

# Get the Channel description
channelDescription = channelSnippet["description"]
channelDescription

# Input the name of channel as a list

channelsList = [
                "channel1",
                "channel2"]

# Loop through each channel and pull data for each channel
ChannelName=[ ]
Description=[ ]
Subscribers=[ ]
TotalVideos=[ ]
TotalViews=[ ]

for channel in channelsList:
    channelUsername= channel
    channelStats = youtube.channels().list(part = "snippet,contentDetails,statistics", forUsername=channelUsername).execute()

    channelStatistics = channelStats["items"][0]["statistics"]

    subscriberCount = channelStatistics["subscriberCount"]
    videoCount = channelStatistics["videoCount"]
    viewCount = channelStatistics["viewCount"]

    channelSnippet =  channelStats["items"][0]["snippet"]
    channelDescription = channelSnippet["description"]

    ChannelName.append(channelUsername)
    Description.append(channelDescription)
    Subscribers.append(subscriberCount)
    TotalVideos.append(videoCount)
    TotalViews.append(viewCount)

data ={"Channel Name" : ChannelName, "Description" : Description, "Subscribers" : Subscribers, "Total Videos" : TotalVideos, "Total Views" : TotalViews}
df=pd.DataFrame(data)

