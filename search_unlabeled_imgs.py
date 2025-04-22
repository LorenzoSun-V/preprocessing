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
    parser.add_argument('--gen', action='store_true', help='generate empty xml labels')
    args = parser.parse_args()
    return args


def create_empty_xml(img_dir, file_name, xml_dir):
    doc = minidom.Document()

    # 创建根元素
    annotation = doc.createElement("annotation")

    # 添加标签信息
    folder = doc.createElement("folder")
    folder.appendChild(doc.createTextNode("images"))  # 图像所在的文件夹名称
    annotation.appendChild(folder)

    filename = doc.createElement("filename")
    filename.appendChild(doc.createTextNode(f"{file_name}.jpg"))  # 图像文件名
    annotation.appendChild(filename)

    path = doc.createElement("path")
    path.appendChild(doc.createTextNode(img_dir))  # 图像的完整路径
    annotation.appendChild(path)

    source = doc.createElement("source")
    database = doc.createElement("database")
    database.appendChild(doc.createTextNode("Unknown"))
    source.appendChild(database)
    annotation.appendChild(source)

    # 创建空的图像尺寸信息
    size = doc.createElement("size")
    height_int, width_int, channel = cv2.imread(img_dir).shape

    width = doc.createElement("width")
    width.appendChild(doc.createTextNode(f"{width_int}"))  # 图像宽度
    size.appendChild(width)

    height = doc.createElement("height")
    height.appendChild(doc.createTextNode(f"{height_int}"))  # 图像高度
    size.appendChild(height)

    depth = doc.createElement("depth")
    depth.appendChild(doc.createTextNode(f"{channel}"))  # 图像通道数
    size.appendChild(depth)

    annotation.appendChild(size)

    seg = doc.createElement("segmented")
    seg.appendChild(doc.createTextNode("0"))
    annotation.appendChild(seg)

    # 将根元素添加到文档
    doc.appendChild(annotation)

    # 生成格式化的XML字符串
    xml_str = doc.toprettyxml(indent="  ")

    # 将XML写入文件
    with open(xml_dir, "w") as xml_file:
        xml_file.write(xml_str)


def search_unlabeled_imgs(root_path, gen_flag):
    unlabeled_list = []
    img_path = osp.join(root_path, "images")
    voc_label_path = osp.join(root_path, "Annotations")
    img_dirs = glob(osp.join(img_path, "*.jpg"))
    img_dirs += glob(osp.join(img_path, "*.png"))
    for img_dir in tqdm(sorted(img_dirs)):
        file_name = osp.basename(img_dir).rsplit('.', 1)[0]
        xml_dir = osp.join(voc_label_path, f"{file_name}.xml")
        if not osp.exists(xml_dir):
            unlabeled_list.append(f"{file_name}\n")
            if gen_flag:
                create_empty_xml(img_dir, file_name, xml_dir)
    if len(unlabeled_list) > 0:
        unlabeled_list_path = osp.join(root_path, "neg_sample.txt")
        with open(unlabeled_list_path, 'w') as f:
            f.writelines(unlabeled_list)


if __name__ == "__main__":
    args = parse_opt()
    search_unlabeled_imgs(args.root_path, args.gen)    
