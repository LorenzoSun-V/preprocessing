'''
Author: BTZN0325 sunjiahui@boton-tech.com
Date: 2023-11-07 16:05:54
LastEditors: BTZN0325 sunjiahui@boton-tech.com
LastEditTime: 2024-01-24 14:22:43
Description: 
'''
# -*- coding:utf-8 -*-
import argparse
import os
import os.path as osp
from glob import glob
from tqdm import tqdm
import xml.etree.cElementTree as ET
import xml.dom.minidom as minidom
import cv2


def parse_opt():
    parser = argparse.ArgumentParser(description="search ublabeled images")
    parser.add_argument('root_path', help='folder path of root_path')
    args = parser.parse_args()
    return args

def search_unlabeled_imgs(root_path):
    img_path = osp.join(root_path, "images")
    label_path = osp.join(root_path, "labels")
    voc_label_path = osp.join(root_path, "voc_labels")
    img_dirs = glob(osp.join(img_path, "*.jpg"))
    img_dirs += glob(osp.join(img_path, "*.png"))

    for img_dir in tqdm(sorted(img_dirs)):
        file_name = osp.basename(img_dir).rsplit('.', 1)[0]
        txt_dir = osp.join(label_path, f"{file_name}.txt")
        if not osp.exists(txt_dir):
            os.system(f"rm {img_dir}")
            xml_dir = osp.join(voc_label_path, f"{file_name}.xml")
            if osp.exists(xml_dir):
                os.system(f"rm {xml_dir}")


if __name__ == "__main__":
    args = parse_opt()
    search_unlabeled_imgs(args.root_path)    

