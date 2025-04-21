import argparse
import os
import cv2
from time import time
from tqdm import tqdm


class VideoFrameExtractor:
    def __init__(self, root_path, out_path, skip_frame=5, jpg_quality=80):
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
                    # 使用初始时间戳和已保存图片的计数器生成文件名
                    path = os.path.join(out_path, f"{start_time:13d}_{saved}.jpg")
                    cv2.imwrite(path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), self.jpg_quality])
                    saved += 1
                rval, frame = vc.read()
                num += 1
        vc.release()

    def filter_video(self):
        """处理视频文件，将每个视频的帧提取为图片"""
        for name in tqdm(os.listdir(self.root_path)):
            src = os.path.join(self.root_path, name)
            out = os.path.join(self.out_path, name.rsplit('.', 1)[0])
            if not os.path.exists(out):
                os.makedirs(out, exist_ok=True)
            if os.path.isfile(src) and name.endswith(self.video_extensions):
                self.v2i(src, out)


def parse_opt():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="Extract frames from videos")
    parser.add_argument('root_path', help='folder path of root_path')
    parser.add_argument('out_path', help='folder path of out_path')
    parser.add_argument('--skip', type=int, default=5, help='skip frame')
    parser.add_argument('--jpg_quality', type=int, default=80, help='jpg quality')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    # 获取命令行参数并创建类实例
    args = parse_opt()
    extractor = VideoFrameExtractor(args.root_path, args.out_path, args.skip, args.jpg_quality)
    extractor.filter_video()
