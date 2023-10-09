import cv2
import os


def folder_iterator(folder: str):
    all_files = os.listdir(f'{folder}')
    for file in all_files:
        if file.endswith('.mp4'):
            video_path = f'{folder}/{file}'
            video_iterator(video_path)


def video_iterator(video_path: str):
    screenshot_path = f'{video_path}_screenshot'
    os.mkdir(f'{screenshot_path}')
    video = cv2.VideoCapture(video_path)

    fps = int(video.get(cv2.CAP_PROP_FPS))
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    for i in range(0, total_frames, fps):
        video.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = video.read()
        if ret:
            cv2.imwrite(f'{screenshot_path}/frame_{i}.jpg', frame)

    # Release video capture
    video.release()


folder_iterator('./videos')
