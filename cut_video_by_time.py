import cv2
import os
import argparse
from datetime import datetime

class VideoExtractor:
    def __init__(self, input_folder, output_folder, videos_dict):
        """
        初始化视频提取器
        :param input_folder: 包含视频文件的输入文件夹
        :param output_folder: 保存提取的视频片段的输出文件夹
        :param videos_dict: 包含视频文件名和时间段的字典
        """
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.videos_dict = videos_dict
        
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def time_to_frame(self, time_str, fps):
        """将时间戳（HH:MM:SS）转换为对应的帧数"""
        t = datetime.strptime(time_str, "%H:%M:%S")
        total_seconds = t.hour * 3600 + t.minute * 60 + t.second
        return int(total_seconds * fps)

    def extract_video_segments(self):
        """根据字典中的时间段批量截取视频片段"""
        for video_name, time_ranges in self.videos_dict.items():
            video_path = os.path.join(self.input_folder, video_name)

            # 打开视频文件
            video_cap = cv2.VideoCapture(video_path)
            if not video_cap.isOpened():
                print(f"Error: Unable to open video {video_name}")
                continue

            # 获取视频的帧率和总帧数
            fps = video_cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))

            # 在输出文件夹创建视频子文件夹
            video_name_without_extension = os.path.splitext(video_name)[0]
            segment_folder = os.path.join(self.output_folder, video_name_without_extension)
            if not os.path.exists(segment_folder):
                os.makedirs(segment_folder)

            for time_range in time_ranges:
                start_time, end_time = time_range.split("-")

                # 转换时间戳为帧数
                start_frame = self.time_to_frame(start_time, fps)
                end_frame = self.time_to_frame(end_time, fps)

                if start_frame >= end_frame:
                    print(f"❌ Warning: Start time {start_time} is greater than or equal to end time {end_time}. Skipping segment.")
                    continue

                # 确保起始帧和结束帧在视频总帧数范围内
                if start_frame >= total_frames:
                    print(f"❌ Warning: Start time {start_time} exceeds the total video duration.")
                    continue

                if end_frame >= total_frames:
                    print(f"❌ Warning: End time {end_time} exceeds the total video duration. Use the end of the video instead.")
                    end_frame = total_frames - 1

                # 设置视频读取的位置
                video_cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

                # 输出分段文件的路径
                segment_filename = os.path.join(segment_folder, f"{video_name_without_extension}_{start_time.replace(':', '')}_{end_time.replace(':', '')}.mp4")
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(segment_filename, fourcc, fps, (int(video_cap.get(3)), int(video_cap.get(4))))

                frame_count = 0
                while frame_count < (end_frame - start_frame):
                    ret, frame = video_cap.read()
                    if not ret:
                        break
                    out.write(frame)
                    frame_count += 1

                out.release()
                print(f"Segment saved: {segment_filename}")

            # 释放视频资源
            video_cap.release()


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="Extract segments from videos based on timestamps")
    parser.add_argument('input_folder', type=str, help="The folder containing the input video files")
    parser.add_argument('output_folder', type=str, help="The folder to store the extracted video segments")
    # parser.add_argument('videos_dict', type=str, help="The dictionary of video files and their timestamp ranges in JSON format")

    return parser.parse_args()


def main():
    # 解析命令行参数
    args = parse_arguments()

    # 将JSON字符串转换为字典
    # import json
    # videos_dict = json.loads(args.videos_dict)
    videos_dict = {
        "1.mp4" : ["00:00:10-00:00:20"]
    }

    # 创建 VideoExtractor 类实例并提取视频片段
    extractor = VideoExtractor(args.input_folder, args.output_folder, videos_dict)
    extractor.extract_video_segments()


if __name__ == "__main__":
    main()
