import sieve
from download_yt import YouTubeDownloader
from split_by_touch import SplitVideoByTouch
from typing import Dict

# super simple function to download a youtube video and return it.
@sieve.workflow(name="video_test_workflow")
def video_test_workflow(url: str) -> sieve.Video:
    yt = YouTubeDownloader(url)     # downloads a youtube video from url, returning a sieve.Video
    return SplitVideoByTouch(yt)    # splits video by touch, only returning first video for now

# https://www.youtube.com/watch?v=etjCVVHlZHs&list=PL_pQQho0KExyLDnVl-JC6VzX3mOug0_sg