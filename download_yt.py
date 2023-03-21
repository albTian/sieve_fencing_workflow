import sieve

@sieve.function(
    name="youtube-downloader",
    gpu = False,
    python_packages=[
        "git+https://github.com/JLeopolt/pytube.git"    # can't use normal pytube yet, it isn't fixed
    ],
    system_packages=[],
    python_version="3.8",
    persist_output=True
)
def YouTubeDownloader(url: str) -> sieve.Video:
    from pytube import YouTube

    yt = YouTube(url)
    if not yt or not yt.streams:
        print("pytube youtube FAIL")
        return
    
    dl_path = yt.streams.get_by_resolution("360p").download(filename="test.mp4")
    print("dl_path")
    print(dl_path)
    return sieve.Video(path=dl_path)
