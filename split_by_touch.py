import sieve


@sieve.function(
    name="split-video-by-touch",
    gpu = False,
    python_packages=[
        "opencv-python"    # can't use normal pytube yet, it isn't fixed
    ],
    system_packages=["libgl1-mesa-glx", "libglib2.0-0", "ffmpeg"],
    python_version="3.8",
    persist_output=True
    # this is actually so stupid but I don't want to use aws cli (would need to configure with private keys)
    # wget doesn't work to get all from /utils...
    run_commands=[
        "mkdir utils",
        # left and right boxes
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/greenbox.png\" > utils/greenbox.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/redbox.png\" > utils/redbox.png",
        
        # score nums
        "mkdir utils/left-score",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/0.png\" > utils/left-score/0.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/1.png\" > utils/left-score/1.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/2.png\" > utils/left-score/2.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/3.png\" > utils/left-score/3.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/4.png\" > utils/left-score/4.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/5.png\" > utils/left-score/5.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/6.png\" > utils/left-score/6.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/7.png\" > utils/left-score/7.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/8.png\" > utils/left-score/8.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/9.png\" > utils/left-score/9.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/10.png\" > utils/left-score/10.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/11.png\" > utils/left-score/11.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/12.png\" > utils/left-score/12.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/13.png\" > utils/left-score/13.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/14.png\" > utils/left-score/14.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/15.png\" > utils/left-score/15.png",

        "mkdir utils/right-score",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/0.png\" > utils/right-score/0.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/1.png\" > utils/right-score/1.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/2.png\" > utils/right-score/2.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/3.png\" > utils/right-score/3.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/4.png\" > utils/right-score/4.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/5.png\" > utils/right-score/5.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/6.png\" > utils/right-score/6.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/7.png\" > utils/right-score/7.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/8.png\" > utils/right-score/8.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/9.png\" > utils/right-score/9.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/10.png\" > utils/right-score/10.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/11.png\" > utils/right-score/11.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/12.png\" > utils/right-score/12.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/13.png\" > utils/right-score/13.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/14.png\" > utils/right-score/14.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/15.png\" > utils/right-score/15.png",
    ]
)
def SplitVideoByTouch(video: sieve.Video) -> str:
    # returns a stream of sieve.Video, representing each touch
    import cv2

    # setup utils (?)


    cap = video.cap     # cap is a property, not a getter function
    cap_end_point = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    position = 0
    while True:
        ret, frame = cap.read()
        if frame is None:
            print("Video finished")
            break
        print(f"position: {position}")
        position += 1
    return "dog"