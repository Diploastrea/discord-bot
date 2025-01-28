import os
from dataclasses import dataclass

import isodate as isodate
from dotenv import load_dotenv
from googleapiclient.discovery import build

from constants import YT_BASE_URL

load_dotenv()
YT_API_KEY = os.getenv('YT_API_KEY')


@dataclass
class Video:
    title: str
    duration: str
    link: str


class YoutubeClient:

    def search(self, query: str, max_results: int = 10):
        youtube = build('youtube', 'v3', developerKey=YT_API_KEY)
        search_response = youtube.search().list(
            q=query,
            part="id,snippet",
            maxResults=max_results,
            type="video"
        ).execute()

        video_ids = [item["id"]["videoId"] for item in search_response.get("items", [])]
        if not video_ids:
            return []

        videos_response = youtube.videos().list(
            part="contentDetails,snippet",
            id=",".join(video_ids)
        ).execute()

        results = []
        for item in videos_response.get("items", []):
            video_title = item["snippet"]["title"]
            if len(video_title) > 85:
                video_title = f'{video_title[:85].strip()}...'
            duration_iso = item["contentDetails"]["duration"]
            duration = self._format_duration(duration_iso)
            video_id = item["id"]
            video_link = YT_BASE_URL + video_id
            results.append(Video(video_title, duration, video_link))

        return results

    @staticmethod
    def _format_duration(duration_iso):
        duration = str(isodate.parse_duration(duration_iso))
        if len(duration) == 7:
            return f'0{duration}'
        else:
            return duration
