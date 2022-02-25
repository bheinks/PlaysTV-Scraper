#!/usr/bin/env python3

from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from sys import exit
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup
from waybackpy import WaybackMachineCDXServerAPI
from waybackpy.exceptions import NoCDXRecordFound

WAYBACK_URL = 'https://web.archive.org/'


@dataclass
class Video:
    url: str
    game: str
    date: datetime
    caption: str
    filename: str


def main(username, download_location):
    profile_url = f'https://plays.tv/u/{username}'
    user_agent = 'PlaysTV Scraper 1.0'
    cdx_api = WaybackMachineCDXServerAPI(profile_url, user_agent)

    try:
        newest_record = cdx_api.newest()
    except NoCDXRecordFound:
        # No record found
        print('ERROR: Archive of profile not found. Exiting...')
        return -1

    videos = get_videos(newest_record.archive_url)
    download_videos(videos, download_location)

    return 0


def get_videos(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    videos = []
    for tag in soup.find_all('video', class_='video-tag'):
        tag = tag.parent

        # Get video page URL
        path = urlparse(tag['href']).path
        page_url = urljoin(WAYBACK_URL, path)

        # Get video object
        video = get_video(page_url)
        videos.append(video)

    return videos


def get_video(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    # Get video URL
    path = soup.find('source', res='720')['src']
    url = urljoin(WAYBACK_URL, path)

    # Get name of video game
    game = soup.find('a', class_='game-link').text

    # Get upload date
    date = soup.find('a', class_='created-time').text
    date = datetime.strptime(date, '%b %d %Y')

    # Get caption
    caption = soup.find('span', class_='description-text').text

    # Construct filename
    filename = f'{date.strftime("%Y-%m-%d")} {caption}{Path(path).suffix}'

    return Video(url, game, date, caption, filename)


def download_videos(videos, download_location):
    for video in videos:
        path = Path(download_location) / video.game
        path.mkdir(parents=True, exist_ok=True)
        file_path = path / video.filename

        r = requests.get(video.url)

        # Write video to file
        with file_path.open('wb') as f:
            f.write(r.content)


if __name__ == '__main__':
    parser = ArgumentParser(description='Scrape the Wayback Machine for archived PlaysTV content.')
    parser.add_argument('username', type=str, help='PlaysTV username')
    parser.add_argument('path', nargs='?', default='.', type=Path,
                        help='video save location (default: current directory)')
    args = parser.parse_args()

    exit(main(args.username, args.path))
