import pandas
from googleapiclient.discovery import build
import config

video_id = 'LgmbgAIebw0'

comments = list()
api_obj = build('youtube', 'v3', developerKey=config.api_key)
response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, maxResults=100).execute()

while response:
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)

        if item['snippet']['totalReplyCount'] > 0:
            for reply_item in item['replies']['comments']:
                reply = reply_item['snippet']['textDisplay']
                comments.append(reply)

    if len(comments)>500:
        break

    if 'nextPageToken' in response:
        response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, pageToken=response['nextPageToken'], maxResults=100).execute()
    else:
        break

df = pandas.DataFrame(comments)
path = './data/'
df.to_csv(path+'comments.txt', index=None, columns=None)