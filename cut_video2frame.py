import argparse
import os
import cv2
from time import time
from tqdm import tqdm


def parse_opt():
    parser = argparse.ArgumentParser(description="search ublabeled images")
    parser.add_argument('root_path', help='folder path of root_path')
    parser.add_argument('out_path', help='folder path of out_path')
    parser.add_argument('--skip', type=int, default=1, help='skip frame')
    parser.add_argument('--jpg_quality', type=int, default=80, help='jpg quality')
    args = parser.parse_args()
    return args


def v2i(src, out_path, jpg_quality, skip_frame):
    vc = cv2.VideoCapture(src)
    num = 0  # 帧计数器
    saved = 0  # 保存的图片计数器
    start_time = int(time()*1000)

    if vc.isOpened():
        rval, frame = vc.read()
        while rval:
            if num % skip_frame == 0:
                # 使用初始时间戳和已保存图片的计数器生成文件名
                path = os.path.join(out_path, f"{start_time:13d}_{saved}.jpg")
                cv2.imwrite(path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])
                saved += 1
            rval, frame = vc.read()
            num += 1
    vc.release()


def filter_video(args):
    root_path = args.root_path
    out_path = args.out_path
    skip_frame = args.skip
    jpg_quality = args.jpg_quality

    assert os.path.exists(root_path), "root_path not exists"
    if not os.path.exists(out_path):
        os.makedirs(out_path, exist_ok=True)
    
    video_extensions = ('.mp4', '.avi', '.mov')  # 定义视频文件的扩展名
    for name in tqdm(os.listdir(root_path)):
        src = os.path.join(root_path, name)
        if os.path.isfile(src) and name.endswith(video_extensions):
            v2i(src, out_path, jpg_quality, skip_frame)


if __name__ == '__main__':
    args = parse_opt()
    filter_video(args)