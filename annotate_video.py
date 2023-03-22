import sieve

@sieve.function(
    name="video-pose-estimation",
    gpu = False,
    python_packages=[
        "opencv-python",    # can't use normal pytube yet, it isn't fixed
        "numpy",
        "tensorflow",
        "tensorflow_hub"
    ],
    system_packages=["libgl1-mesa-glx", "libglib2.0-0", "ffmpeg"],
    python_version="3.8",
    persist_output=True,
    # iterator_input=True
)
def AnnotateVideo(video: sieve.Video) -> sieve.Video:
    import cv2
    import numpy as np
    import tensorflow as tf
    import tensorflow_hub as hub
    import os

    print("annotating video")
    print(video)

    # abstract this into a sieve.model?
    model = hub.load("https://tfhub.dev/google/movenet/multipose/lightning/1")
    movenet = model.signatures['serving_default']

    def loop_through_people(frame, keypoints_with_scores, edges, confidence_threshold):
        for person in keypoints_with_scores:
            draw_connections(frame, person, edges, confidence_threshold)
            draw_keypoints(frame, person, confidence_threshold)

    def draw_keypoints(frame, keypoints, confidence_threshold):
        y, x, c = frame.shape
        shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
        
        for kp in shaped:
            ky, kx, kp_conf = kp
            if kp_conf > confidence_threshold:
                cv2.circle(frame, (int(kx), int(ky)), 2, (0,255,0), -1)

    def draw_connections(frame, keypoints, edges, confidence_threshold):
        y, x, c = frame.shape
        shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
        
        for edge, color in edges.items():
            p1, p2 = edge
            y1, x1, c1 = shaped[p1]
            y2, x2, c2 = shaped[p2]
            
            if (c1 > confidence_threshold) & (c2 > confidence_threshold):      
                cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,255), 1)

    EDGES = {
        (0, 1): 'm',
        (0, 2): 'c',
        (1, 3): 'm',
        (2, 4): 'c',
        (0, 5): 'm',
        (0, 6): 'c',
        (5, 7): 'm',
        (7, 9): 'm',
        (6, 8): 'c',
        (8, 10): 'c',
        (5, 6): 'y',
        (5, 11): 'm',
        (6, 12): 'c',
        (11, 12): 'y',
        (11, 13): 'm',
        (13, 15): 'm',
        (12, 14): 'c',
        (14, 16): 'c'
    }
    output_path = "/root/videos-annotated/"
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    cap = video.cap
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    annotated_frames = []
    while cap.isOpened():
        ret, frame = cap.read()

        if frame is None:
            break
        
        # Resize image
        img = frame.copy()
        img = tf.image.resize_with_pad(tf.expand_dims(img, axis=0), 384,640)
        input_img = tf.cast(img, dtype=tf.int32)
        
        # Detection section
        results = movenet(input_img)
        keypoints_with_scores = results['output_0'].numpy()[:,:,:51].reshape((6,17,3))
        
        # Render keypoints 
        loop_through_people(frame, keypoints_with_scores, EDGES, 0.4) #0.4 is our confidence_threshold
        
        annotated_frames.append(frame)

    # Create a VideoWriter object for the output video
    output_file = f"{output_path}temp.mp4"
    output_file_h264 = f"{output_path}test.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    # Write the frames to the output video
    for frame in annotated_frames:
        writer.write(frame)
    # Release the output video
    writer.release()
    os.system(f"ffmpeg -i {output_file} -vcodec libx264 -f mp4 {output_file_h264}")     # convert so its viewable in browser

    cap.release()
    # cv2.destroyAllWindows()

    return sieve.Video(path=output_file_h264)


