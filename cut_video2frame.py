import argparse
import os
import cv2
from time import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed


class VideoFrameExtractor:
    def __init__(self, root_path, out_path, skip_frame=5, jpg_quality=80, workers=8):
        """
        初始化类，设置输入和输出路径、跳过帧数和JPG质量
        :param root_path: 输入视频文件夹路径
        :param out_path: 输出图片文件夹路径
        :param skip_frame: 跳过的帧数
        :param jpg_quality: JPG图片的质量
        """
        self.root_path = root_path
        self.out_path = out_path
        self.skip_frame = skip_frame
        self.jpg_quality = jpg_quality
        self.workers = workers

        # 检查输入路径是否存在
        assert os.path.exists(self.root_path), "root_path does not exist"
        # 如果输出路径不存在，创建它
        if not os.path.exists(self.out_path):
            os.makedirs(self.out_path, exist_ok=True)

        self.video_extensions = ('.mp4', '.avi', '.mov')

    def v2i(self, src, out_path):
        """将视频转换为图片，并保存到指定目录"""
        vc = cv2.VideoCapture(src)
        num = 0  # 帧计数器
        saved = 0  # 保存的图片计数器
        start_time = int(time() * 1000)

        if vc.isOpened():
            rval, frame = vc.read()
            while rval:
                if num % self.skip_frame == 0:
                    path = os.path.join(out_path, f"{start_time:013d}_{saved}.jpg")
                    cv2.imwrite(path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), self.jpg_quality])
                    saved += 1
                rval, frame = vc.read()
                num += 1
        vc.release()

    def filter_video(self):
        """使用多线程处理视频文件，将每个视频的帧提取为图片"""
        video_tasks = []
        with ThreadPoolExecutor(max_workers=self.workers) as executor:  # 可根据需求调整 max_workers
            for name in os.listdir(self.root_path):
                src = os.path.join(self.root_path, name)
                out = os.path.join(self.out_path, name.rsplit('.', 1)[0])
                if os.path.isfile(src) and name.endswith(self.video_extensions):
                    if not os.path.exists(out):
                        os.makedirs(out, exist_ok=True)
                    video_tasks.append(executor.submit(self.v2i, src, out))

            for future in tqdm(as_completed(video_tasks), total=len(video_tasks), desc="Processing Videos"):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error processing a video: {e}")


def parse_opt():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="Extract frames from videos")
    parser.add_argument('root_path', help='folder path of root_path')
    parser.add_argument('out_path', help='folder path of out_path')
    parser.add_argument('--skip', type=int, default=5, help='skip frame')
    parser.add_argument('--jpg_quality', type=int, default=80, help='jpg quality')
    parser.add_argument('--workers', type=int, default=8, help='workers')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_opt()
    extractor = VideoFrameExtractor(args.root_path, args.out_path, args.skip, args.jpg_quality)
    extractor.filter_video()