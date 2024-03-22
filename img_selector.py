import fastdeploy as fd
import cv2
import os
import os.path as osp
import numpy as np
from glob import glob
from tqdm import tqdm
import shutil


class ImgSelector:
    def __init__(self, 
                 model_path,
                 img_path,
                 save_path) -> None:
        self.model = self.load_model(model_path)
        self.img_list = self.load_img(img_path)
        self.select(save_path)
    
    def check_path(self, path):
        assert osp.exists(path), f"{path} is not existed!"

    def load_model(self, model_path):
        self.check_path(model_path)
        if "yolov5" in model_path:
            return fd.vision.detection.YOLOv5(model_path)
        elif "yolov8" in model_path:
            return fd.vision.detection.YOLOv8(model_path)
    
    def load_img(self, img_path):
        self.check_path(img_path)
        image_extensions = ['*.jpg', '*.jpeg', '*.png', "*.bmp", "*.tiff", "*.tif", "*.JPG", "*.JPEG", "*.PNG", "*.BMP", "*.TIFF", "*.TIF"]
        img_list = []
        for extension in image_extensions:
            img_list.extend(glob(os.path.join(img_path, extension)))
        return img_list
    
    def select(self, save_path):
        if not osp.exists(save_path):
            os.makedirs(save_path, exist_ok=True)
        for img_path in tqdm(self.img_list):
            img_name = osp.basename(img_path)
            img_save_path = osp.join(save_path, img_name)
            img = cv2.imread(img_path)
            result = self.model.predict(img)
            if len(result.boxes) > 0:
                shutil.copy(img_path, img_save_path)


model_path = "/home/sysadmin/lorenzo/bt_repo/yolov5/yolov5-v7.0/runs/xray-gs/yolov5s-v7.0_20240321_cls4_xray-gs-sub_v0.1/weights/best.onnx"
img_path = "/data/bt/xray_gangsi/raw_zips/20240320_liyang/normal"
save_path = "/data/bt/xray_gangsi/raw_zips/20240320_liyang/select"
selector = ImgSelector(model_path, img_path, save_path)