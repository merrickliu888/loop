import requests

def get_youtube_videos(query: str):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&q={query}&key={API_KEY}"
    response = requests.get(url)
    return response.json()