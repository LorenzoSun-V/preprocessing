'''
Author: BTZN0325 sunjiahui@boton-tech.com
Date: 2023-11-07 16:05:54
LastEditors: BTZN0325 sunjiahui@boton-tech.com
LastEditTime: 2023-12-12 10:23:44
Description: 
'''
import os
import os.path as osp
import shutil
import cv2
from glob import glob
from time import time
from tqdm import tqdm


def rename(file_name_ext, index):
    """
    Args:
        file_name_ext (str): file name with extension, like 'abc.192.168.2.2.jpg'
    Return:
        new_name (str): new file name without extension, like '1897643513123_1'
    """
    timestamp = int(time()*1000)
    file_name_stem = file_name_ext.rsplit('.', 1)[0]
    new_name = f"{timestamp:13d}-{index}_{file_name_stem}"
    return new_name



if __name__ == "__main__":
    root_dirs = ["/data/bt/xray_fanglun/LabeledData/20240228/images", "/data/bt/xray_fanglun/LabeledData/20240228/images_re"]
    label_ext = "json"
    for root_dir in tqdm(root_dirs):
        img_dirs = sorted(glob(osp.join(root_dir, "*.[jJ][pP][gG]*")) + glob(osp.join(root_dir, "*.[jJ][pP][eE][gG]*")) + glob(osp.join(root_dir, "*.[pP][nN][gG]*")))
        for index, img_dir in tqdm(enumerate(img_dirs)):
            img_dirname = osp.dirname(img_dir)
            img_name_ext = osp.basename(img_dir)
            ext = img_name_ext.rsplit('.', 1)[-1]
            label_dir = osp.join(img_dirname, f"{img_name_ext.replace(ext, label_ext)}")
            new_name = rename(img_name_ext, index)
            new_img_dir = osp.join(img_dirname, f"{new_name}.jpg")
            new_label_dir = osp.join(img_dirname, f"{new_name}.json")
            os.rename(img_dir, new_img_dir)
            if osp.exists(label_dir):
                os.rename(label_dir, new_label_dir)
            else:
                print(f"{label_dir} is not existed!")