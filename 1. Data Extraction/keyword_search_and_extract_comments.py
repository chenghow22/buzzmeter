# Setup and import library
from googleapiclient.discovery import build
import pandas as pd

# Setup your youtube api key
youTubeApiKey = "AIzaSyAHUUYyzidO-SkbGiBc_9ZO7JkaxJHXZYc"
youtube = build("youtube","v3",developerKey = youTubeApiKey)

# Define your search query
search_query = 'Counter-Strike: Global Offensive'

# Perform the search
search_response = youtube.search().list(
    q=search_query + ' review',
    type='video',
    part='id',
    maxResults=10  # You can adjust this to retrieve more or fewer results
    #order='date'  # Sort by date to prioritize the latest published videos (too few comment for those latest videos)
).execute()

video_ids = []

# Iterate through the search results
for item in search_response['items']:
    video_id = item['id']['videoId']

    # Fetch video statistics to check view count and comment count
    video_stats = youtube.videos().list(
        part='statistics',
        id=video_id
    ).execute()

    # Fetch the video's publish date
    video_snippet = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()

    # Get the video's publish date as a datetime object (assuming UTC timezone)
    publish_date = datetime.fromisoformat(video_snippet['items'][0]['snippet']['publishedAt'].replace('Z', '+00:00'))

    # Make the publish_date timezone-aware (assuming UTC)
    publish_date = publish_date.replace(tzinfo=pytz.UTC)

    # Calculate the date 5 years ago from today
    five_years_ago = datetime.now() - timedelta(days=365 * 5)

    # Make the five_years_ago datetime timezone-aware (assuming UTC)
    five_years_ago = five_years_ago.replace(tzinfo=pytz.UTC)

    # Check if the video meets the criteria:
    # 1. View count > 10k
    # 2. Comment count > 100
    # 3. Published date is less than 5 years from now
    if (#int(video_stats['items'][0]['statistics']['viewCount']) > 5000 and
        #int(video_stats['items'][0]['statistics']['commentCount']) > 100 and
        publish_date >= five_years_ago):

          video_ids.append(video_id)

# Print the video IDs
for video_id in video_ids:
    print(f'Video ID: {video_id}')

# Initialize a list to store comments and other attributes
id_conso = []
comment_conso = []
updated_conso = []
like_conso = []
comment_id_conso = []

# Define parameters for comment retrieval
params = {
    'maxResults': 300,  # Adjust the number of results per page as needed
    'order': 'relevance',  # Default is 'time' (newest)
}

# Define the number of pages to retrieve
n_pages = 5  # Adjust as needed

# Iterate through the video IDs
for video_id in video_ids:



  params['videoId'] = video_id

  for i in range(n_pages):

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
                next_page_token = response["nextPageToken"]
            else:
                break

        # except Exception as e:
        #     print(f'Error fetching comments for video ID: {video_id}')
        #     print(f'Error message: {str(e)}')

# Print the total number of comments extracted
print(f'Total number of comments extracted: {len(comment_conso)}')

# Putting the information into a dataframe
data = {'date':updated_conso,'video_id':id_conso,'comment':comment_conso,'like_count':like_conso,'comment_id':comment_id_conso}
df = pd.DataFrame(data)