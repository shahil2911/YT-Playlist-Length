# from googleapiclient.discovery import build
# import re
# import isodate
# import math
# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Your Google API key
# API_KEY = os.getenv('API_KEY')

# # Build a service object for interacting with the API
# youtube = build('youtube', 'v3', developerKey=API_KEY)

# def get_playlist_id(url):
#     """Extract playlist ID from YouTube URL."""
#     if 'list=' in url:
#         return re.findall(r"list=([a-zA-Z0-9_-]+)", url)[0]
#     return None

# def get_playlist_videos(playlist_id):
#     """Retrieve videos from the given playlist ID."""
#     videos = []
#     next_page_token = None

#     while True:
#         pl_request = youtube.playlistItems().list(
#             part='contentDetails',
#             playlistId=playlist_id,
#             maxResults=50,
#             pageToken=next_page_token
#         )
#         pl_response = pl_request.execute()

#         videos += [item['contentDetails']['videoId'] for item in pl_response['items']]

#         next_page_token = pl_response.get('nextPageToken')

#         if not next_page_token:
#             break

#     return videos

# def get_video_durations(video_ids):
#     """Get the durations of the given video IDs."""
#     total_duration = 0
#     for i in range(0, len(video_ids), 50):
#         vid_request = youtube.videos().list(
#             part="contentDetails",
#             id=','.join(video_ids[i:i+50])
#         )
#         vid_response = vid_request.execute()

#         for item in vid_response['items']:
#             duration = isodate.parse_duration(item['contentDetails']['duration'])
#             total_duration += duration.total_seconds()

#     return total_duration



# def seconds_to_hms(seconds):
#     """Convert seconds to hours, minutes, and seconds."""
#     hours = seconds // 3600
#     minutes = (seconds % 3600) // 60
#     seconds = seconds % 60
#     return int(hours), int(minutes), int(seconds)

# def format_duration(hours, minutes, seconds):
#     """Format the duration into a string."""
#     return f"{hours} hours, {minutes} minutes, {seconds} seconds"

# def main():
#     url = input("Enter the URL of the YouTube playlist: ")
#     playlist_id = get_playlist_id(url)
#     if not playlist_id:
#         print("Invalid YouTube URL or Playlist ID.")
#         return

#     video_ids = get_playlist_videos(playlist_id)
#     total_duration_in_seconds = get_video_durations(video_ids)
#     total_duration_hours, total_duration_minutes, total_duration_seconds = seconds_to_hms(total_duration_in_seconds)
#     print("Number of videos: %d" % len(video_ids))
#     if len(video_ids) > 0:
#         avg_duration = total_duration_in_seconds / len(video_ids)  # Ensure division is done on total seconds
#         avg_hours, avg_minutes, avg_seconds = seconds_to_hms(avg_duration)
#         print(f"Average duration per video: {format_duration(avg_hours, avg_minutes, avg_seconds)}")
#     else:
#         print("No videos found in the playlist.")

#     print(f"Total length of playlist: {format_duration(total_duration_hours, total_duration_minutes, total_duration_seconds)}")

#     # Calculate durations at different speeds
#     speeds = [1.25, 1.5, 1.75, 2.0]
#     for speed in speeds:
#         adjusted_seconds = math.floor(total_duration_in_seconds / speed)
#         hours, minutes, seconds = seconds_to_hms(adjusted_seconds)
#         print(f"At {speed}x: {format_duration(hours, minutes, seconds)}")

# if __name__ == "__main__":
#     main()

from flask import Flask, request, render_template
from googleapiclient.discovery import build
import re
import isodate
import math
# import os
# from dotenv import load_dotenv


# app = Flask(__name__)

# # Load environment variables from .env file
# load_dotenv()

# Your Google API key
API_KEY = api_key


# Build a service object for interacting with the API
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_playlist_id(url):
    """Extract playlist ID from YouTube URL."""
    if 'list=' in url:
        return re.findall(r"list=([a-zA-Z0-9_-]+)", url)[0]
    return None

def get_playlist_videos(playlist_id):
    """Retrieve videos from the given playlist ID."""
    videos = []
    next_page_token = None
    while True:
        pl_request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        pl_response = pl_request.execute()
        videos += [item['contentDetails']['videoId'] for item in pl_response['items']]
        next_page_token = pl_response.get('nextPageToken')
        if not next_page_token:
            break
    return videos

def get_video_durations(video_ids):
    """Get the durations of the given video IDs."""
    total_duration = 0
    for i in range(0, len(video_ids), 50):
        vid_request = youtube.videos().list(
            part="contentDetails",
            id=','.join(video_ids[i:i+50])
        )
        vid_response = vid_request.execute()
        for item in vid_response['items']:
            duration = isodate.parse_duration(item['contentDetails']['duration'])
            total_duration += duration.total_seconds()
    return total_duration

def calculate_adjusted_durations(total_seconds, speeds):
    results = {}
    for speed in speeds:
        adjusted_seconds = total_seconds / speed
        hours, minutes, seconds = map(int, [adjusted_seconds // 3600, (adjusted_seconds % 3600) // 60, adjusted_seconds % 60])
        results[speed] = f"{hours} hours, {minutes} minutes, {seconds} seconds"
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        playlist_id = get_playlist_id(url)
        if playlist_id:
            video_ids = get_playlist_videos(playlist_id)
            total_duration_seconds = get_video_durations(video_ids)
            hours, minutes, seconds = map(int, [total_duration_seconds // 3600, (total_duration_seconds % 3600) // 60, total_duration_seconds % 60])
            duration = f"{hours} hours, {minutes} minutes, {seconds} seconds"

            avg_duration_seconds = total_duration_seconds / len(video_ids)
            avg_hours, avg_minutes, avg_seconds = map(int, [avg_duration_seconds // 3600, (avg_duration_seconds % 3600) // 60, avg_duration_seconds % 60])
            avg_duration = f"{avg_hours} hours, {avg_minutes} minutes, {avg_seconds} seconds"

            speeds = [1.25, 1.5, 1.75, 2.0]
            adjusted_durations = calculate_adjusted_durations(total_duration_seconds, speeds)
            return render_template('index.html', duration=duration, number_of_videos=len(video_ids), avg_duration=avg_duration, adjusted_durations=adjusted_durations)
        else:
            return render_template('index.html', error="Invalid YouTube URL or Playlist ID.")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
