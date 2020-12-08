import datetime
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from apikey import apikey

CLIENT_SECRET_FILE = 'client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
credentials = flow.run_console()
youtube = build('youtube', 'v3', credentials=credentials)

upload_date_time = datetime.datetime(2029, 8, 25, 12, 30, 0).isoformat() + '.000Z'

request_body = {
    'snippet': {
        'categoryI': 19,
        'title': 'Upload Testing This is Private Video ',
        'description': 'Upload TEsting This is Private Video'
    },
    'status': {
        'privacyStatus': 'private',
        'publishAt': upload_date_time,
        'selfDeclaredMadeForKids': False, 
    },
    'notifySubscribers': False
}

mediaFile = MediaFileUpload('/root/youtube/1.avi', chunksize=1024*1024, resumable=True)

response_upload = youtube.videos().insert(
    part='snippet,status',
    body=request_body,
    media_body=mediaFile
).execute()

youtube.thumbnails().set(
    videoId=response_upload.get('id'),
    media_body=MediaFileUpload('/root/youtube/thumbnail.png', chunksize=1024*1024, resumable=True)
).execute()
