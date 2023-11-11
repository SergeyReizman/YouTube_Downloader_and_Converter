import pytube
import logging

# Constants for resolutions
LOW_RESOLUTION = 18
MEDIUM_RESOLUTION = 22
HIGH_RESOLUTION = 137
VERY_HIGH_RESOLUTION = 313

def download_video(url, resolution):
    try:
        itag = choose_resolution(resolution)
        video = pytube.YouTube(url)
        stream = video.streams.get_by_itag(itag)
        print(f"Downloading: {video.title} ({resolution})")
        stream.download()
        print(f"Download complete: {stream.default_filename}")
        return stream.default_filename
    except pytube.exceptions.RegexMatchError:
        logging.error(f"Invalid URL: {url}")
    except pytube.exceptions.VideoUnavailable:
        logging.error(f"Video is unavailable: {url}")

def download_videos(urls, resolution):
    for url in urls:
        download_video(url, resolution)

def download_playlist(url, resolution):
    try:
        playlist = pytube.Playlist(url)
        download_videos(playlist.video_urls, resolution)
    except pytube.exceptions.RegexMatchError:
        logging.error(f"Invalid playlist URL: {url}")
    except pytube.exceptions.VideoUnavailable:
        logging.error(f"Playlist is unavailable: {url}")

def choose_resolution():
    resolution_choices = {
        "low": LOW_RESOLUTION,
        "medium": MEDIUM_RESOLUTION,
        "high": HIGH_RESOLUTION,
        "very high": VERY_HIGH_RESOLUTION,
    }

    print("Choose resolution:")
    for choice, itag in resolution_choices.items():
        print(f"{choice.capitalize()}: {itag}")

    resolution = input("Enter your choice: ").lower()
    return resolution_choices.get(resolution, LOW_RESOLUTION)

def input_links():
    print("Enter the links of the videos (end by entering 'STOP'):")

    links = []
    link = ""

    while link.lower() != "stop":
        link = input()
        if link.lower() != "stop":
            links.append(link)

    return links

if __name__ == "__main__":
    logging.basicConfig(filename='download.log', level=logging.INFO)
    resolution = choose_resolution()
    urls = input_links()

    if urls:
        download_videos(urls, resolution)
    else:
        print("No valid links provided.")
