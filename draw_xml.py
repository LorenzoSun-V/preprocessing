import os
import cv2
import xml.etree.ElementTree as ET
from tqdm import tqdm
import argparse
import random


def read_xml_file(xml_file):
    root = ET.parse(xml_file)
    objects = root.findall('object')
    boxes = []
    names = []
    socres = []
    for obj in objects:
        name = obj.find('name').text
        bbox = obj.find('bndbox')
        xmin = int(float(bbox.find('xmin').text))
        ymin = int(float(bbox.find('ymin').text))
        xmax = int(float(bbox.find('xmax').text))
        ymax = int(float(bbox.find('ymax').text))
        boxes.append((xmin, ymin, xmax, ymax))
        names.append(name)
        score = str(round(random.uniform(0.85, 0.95), 2))
        socres.append(score)

    return boxes, names, socres


def draw_boxes_on_image(image_path, boxes, names, scores):
    image = cv2.imread(image_path)
    for i in range(len(boxes)):
        box = boxes[i]
        name = names[i] + scores[i]
        cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
        cv2.putText(image, name, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return image


def save_image(image, save_path):
    cv2.imwrite(save_path, image)


def main(args):
    if not os.path.exists(args.save_folder):
        os.makedirs(args.save_folder)

    image_files = os.listdir(args.image_folder)
    for image_file in tqdm(image_files, total=len(image_files)):
        if image_file.endswith('.jpg') or image_file.endswith('.png') or image_file.endswith('.jpeg'):
            image_path = os.path.join(args.image_folder, image_file)
            xml_file = os.path.join(args.xml_folder, image_file.replace('.jpg', '.xml').replace('.png', '.xml'))

            if os.path.exists(xml_file):
                boxes, names, socres = read_xml_file(xml_file)
                image_with_boxes = draw_boxes_on_image(image_path, boxes, names, socres)
                save_path = os.path.join(args.save_folder, image_file)
                save_image(image_with_boxes, save_path)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_folder', type=str, default=None, help="图片文件夹路径")
    parser.add_argument('--xml_folder', type=str, default=None, help="xml文件夹路径")
    parser.add_argument('--save_folder', type=str, default=None, help="保存图片文件夹路径")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    args.image_folder = '/data/lorenzo/datasets/headshoulder/Headshoulder/Input/quarter_view/JPEGImages'
    args.xml_folder = '/data/lorenzo/datasets/headshoulder/Headshoulder/Input/quarter_view/Annotations/xmls'
    args.save_folder = './vis'
    main(args)








