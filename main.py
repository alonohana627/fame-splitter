import cv2
import os
import shutil
from pathlib import Path
import sys

videos_path = ""

if len(sys.argv) == 1:
    videos_path = "./videos"
else:
    videos_path = sys.argv[1]

# if videos_path == None:
#     print("Videos Path ENV does not exist")
#     exit(1)

if videos_path is None:
    videos_path = "./videos"

finished_videos = os.path.join(videos_path, "finished_videos")
unfinished_videos = os.path.join(videos_path, "unfinished_videos")
screenshot_path = os.path.join(videos_path, "screenshots")

Path(finished_videos).mkdir(exist_ok=True)
Path(unfinished_videos).mkdir(exist_ok=True)
Path(screenshot_path).mkdir(exist_ok=True)

print("Video Frame Splitter")
print("=====================")


def folder_iterator(folder: str):
    all_files = os.listdir(f'{folder}')
    extensions = ['mp4', 'avi']  # TODO: add more formats
    video_files = [f for f in all_files if any(f.endswith(ext) for ext in extensions)]

    print(f"There are {len(video_files)} videos to process\n")

    for index, file in enumerate(video_files):
        print(f"{index + 1}/{len(video_files)}: Currently processing {file}...")
        video_path = f'{folder}/{file}'
        result = video_iterator(video_path, file)

        if result is True:
            print(f"{index + 1}/{len(video_files)}: DONE!\n")
        else:
            print(f"{index + 1}/{len(video_files)}: {file} is not done. Moved to unfinished videos folder")


def video_iterator(video_path: str, file_name: str):
    video = cv2.VideoCapture(video_path)

    fps = int(video.get(cv2.CAP_PROP_FPS))
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    for i in range(0, total_frames, fps):
        video.set(cv2.CAP_PROP_POS_FRAMES, i)
        result = video.grab()
        if result is False:
            video.release()
            shutil.move(video_path, unfinished_videos)
            return False

        ret, frame = video.retrieve()

        if ret:
            cv2.imwrite(f'{screenshot_path}/{file_name}_frame_{i}.jpg', frame)

    # Release video capture
    video.release()
    shutil.move(video_path, finished_videos)
    return True


folder_iterator(videos_path)
