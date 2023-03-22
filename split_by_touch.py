import sieve
from typing import List


@sieve.function(
    name="split-video-by-touch",
    gpu = False,
    python_packages=[
        "opencv-python",    # can't use normal pytube yet, it isn't fixed
        "numpy"
    ],
    system_packages=["libgl1-mesa-glx", "libglib2.0-0", "ffmpeg"],
    python_version="3.8",
    persist_output=True,
    # this is actually so stupid but I don't want to use aws cli (would need to configure with private keys)
    # wget doesn't work to get all from /utils...
    run_commands=[
        "mkdir /root/utils",
        # left and right boxes
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/greenbox.png\" > /root/utils/greenbox.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/redbox.png\" > /root/utils/redbox.png",

        # score nums
        "mkdir /root/utils/left-score",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/0.png\" > /root/utils/left-score/0.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/1.png\" > /root/utils/left-score/1.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/2.png\" > /root/utils/left-score/2.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/3.png\" > /root/utils/left-score/3.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/4.png\" > /root/utils/left-score/4.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/5.png\" > /root/utils/left-score/5.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/6.png\" > /root/utils/left-score/6.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/7.png\" > /root/utils/left-score/7.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/8.png\" > /root/utils/left-score/8.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/9.png\" > /root/utils/left-score/9.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/10.png\" > /root/utils/left-score/10.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/11.png\" > /root/utils/left-score/11.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/12.png\" > /root/utils/left-score/12.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/13.png\" > /root/utils/left-score/13.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/14.png\" > /root/utils/left-score/14.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/left-score/15.png\" > /root/utils/left-score/15.png",

        "mkdir /root/utils/right-score",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/0.png\" > /root/utils/right-score/0.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/1.png\" > /root/utils/right-score/1.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/2.png\" > /root/utils/right-score/2.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/3.png\" > /root/utils/right-score/3.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/4.png\" > /root/utils/right-score/4.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/5.png\" > /root/utils/right-score/5.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/6.png\" > /root/utils/right-score/6.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/7.png\" > /root/utils/right-score/7.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/8.png\" > /root/utils/right-score/8.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/9.png\" > /root/utils/right-score/9.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/10.png\" > /root/utils/right-score/10.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/11.png\" > /root/utils/right-score/11.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/12.png\" > /root/utils/right-score/12.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/13.png\" > /root/utils/right-score/13.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/14.png\" > /root/utils/right-score/14.png",
        "curl \"https://fencing-utils.s3.us-west-1.amazonaws.com/utils/right-score/15.png\" > /root/utils/right-score/15.png"
    ]
)
def SplitVideoByTouch(video: sieve.Video) -> sieve.Video:
    # returns a stream of sieve.Video, representing each touch
    import cv2
    import numpy as np
    import os

    output_path = "/root/videos-cut/"
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # helper functions (can I define these outside of this func?)
    def compare_pics(reference, tester):
        return np.sum(abs(reference - tester))

    def score(pics, frame):
        min_diff = 100000
        score = -1
        for i in range(16):
            if i < 0 or i > 15:
                continue
            test_pic = pics[i]
            diff = compare_pics(frame, test_pic)
            if diff < min_diff:
                min_diff = diff
                score = i
        
        return score

    # starting at POSITION, record LENGTH frames.
    # cap will maintain its position before/after this call
    def record_touch(cap, position, length, clip_num, left_score, right_score) -> sieve.Video:
        old_pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        cap.set(1, position)

        # Collect frames
        frames = []
        for _ in range(length):
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)

        # Create a VideoWriter object for the output video
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        output_file = f"{output_path}test-{clip_num}[{left_score}-{right_score}].mp4"
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

        # Write the frames to the output video
        for frame in frames:
            writer.write(frame)

        # Release the output video
        writer.release()
        cap.set(1, old_pos)    # reset the position (so before/after this function is the same)
        sv_vid = sieve.Video(path=output_file)
        # print(f"output_file: {output_file}, frames: {sv_vid.frame_count}")
        return sv_vid

    # setup utils (?)
    green_box = cv2.imread("/root/utils/greenbox.png")
    red_box = cv2.imread("/root/utils/redbox.png")
    green_box_int = green_box.astype(int)
    red_box_int = red_box.astype(int)
    left_pics = [cv2.imread("/root/utils/left-score/{}.png".format(i)) for i in range(0, 16)]
    right_pics = [cv2.imread("/root/utils/right-score/{}.png".format(i)) for i in range(0, 16)]


    # setup video
    clips_recorded = 0
    position, position_skip = 360, True     # skip the beginning, nothing happening

    cap = video.cap     # cap is a property, not a getter function
    cap_end_point = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap_end_point -= 260    # ensures videos don't overrun
    left_score = right_score = left_score_last = right_score_last = 0
    result_vids = []

    while position < cap_end_point:
        
        if not cap.isOpened():
            print("Failed to open video")
            break

        if position_skip:
            cap.set(1,position)
            position_skip = False

        # while cap.isOpened():
        ret,frame = cap.read()
        position += 1

        if frame is None:
            print("video done")
            break

        # based off frames of 640*360 video on fie stream
        red_light = (np.sum(abs(frame[330:334, 140:260].astype(int)-red_box_int)) <= 40000)
        green_light = (np.sum(abs(frame[330:334, 380:500].astype(int)-green_box_int)) <= 40000)

        
        if red_light or green_light:
            # print("light!")
            # go back 60 frames (2 seconds) and record
            # record the last 60 seconds. Can add logic for testing blades later
            left_frame = frame[310:310+15, 265:265+19].astype(int)
            right_frame = frame[310:310+15, 356:356+19].astype(int)

            left_score = score(left_pics, left_frame)
            right_score = score(right_pics, right_frame)

            if left_score_last is not left_score or right_score_last is not right_score:
                left_score_last, right_score_last = left_score, right_score
            
            # record 60 frames before, 30 frames after (90 total)
            touch_vid = record_touch(cap, position-60, 90, clips_recorded, left_score, right_score)
            print(touch_vid)
            result_vids.append(touch_vid)
            clips_recorded += 1
            position += 260     # skip the light staying on, plus fencers getting back en guarde 
            position_skip = True
            # break


        # print(position)
    # record a touch of length from an open cap at position
    cap.release()
    return result_vids[0]

    # upload to s3
