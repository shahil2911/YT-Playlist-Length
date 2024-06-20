# YouTube Playlist Length Calculator

This Flask application calculates the total duration of a YouTube playlist, providing insights such as the number of videos, average video length, and adjusted durations at different playback speeds.

## Features

- **Playlist Duration Calculation**: Enter a YouTube playlist URL to get the total duration of all videos in the playlist.
- **Detailed Insights**: View the number of videos in the playlist, average video length, and total duration.
- **Playback Speed Adjustments**: Calculate how long it would take to watch the entire playlist at different speeds (1.25x, 1.5x, 1.75x, and 2.0x).

## How It Works

The application uses the YouTube Data API to fetch playlist details and compute durations. Here's a brief overview of the process:

1. **Extract Playlist ID**: The playlist ID is extracted from the provided YouTube URL.
2. **Retrieve Video IDs**: All video IDs within the playlist are retrieved using the YouTube Data API.
3. **Calculate Durations**: The duration of each video is fetched and summed up to get the total duration.
4. **Adjust Durations**: Durations are adjusted based on different playback speeds.

## Prerequisites

Before you can run the application, you need to have the following installed:
- Python 3
- Flask
- Google API Client Library for Python

Additionally, you will need a valid Google API key with access to the YouTube Data API.

## Setup

1. **Clone the Repository**:
   
```bash
   git clone https://github.com/shahil2911/youtube-playlist-length-calculator.git
   cd youtube-playlist-length-calculator
