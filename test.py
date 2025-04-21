import os
from glob import glob
import cv2
import json
import shutil
import xml.etree.ElementTree as ET
from xml.dom import minidom
from tqdm import tqdm
import ultralytics

img_dir = "/data/public/coco_person/images"
label_dir = "/data/public/coco_person/labels"
img_dest_dir = "/data/nofar/data_person/v0.1/images" 
label_dest_dir = "/data/nofar/data_person/v0.1/labels"

for folder in ["train2017", "val2017"]:
    img_folder = os.path.join(img_dir, folder)
    label_folder = os.path.join(label_dir, folder)
    for img in tqdm(os.listdir(img_folder)):
        img_path = os.path.join(img_folder, img)
        shutil.copy(img_path, img_dest_dir)
    for label in tqdm(os.listdir(label_folder)):
        label_path = os.path.join(label_folder, label)
        shutil.copy(label_path, label_dest_dir)


# for belt in os.listdir(root_path):
#     cur_belt = os.path.join(root_path, belt)
#     for img in os.listdir(cur_belt):
#         if img.split('.')[1] != 'jpg':
#             continue
#         img_path = os.path.join(cur_belt, img)
#         img_name = img.split('.')[0]
#         json_dir = json_dict[img_name]
#         with open(json_dir, 'r', encoding='utf-8') as f:
#             data = json.load(f)
#             data['imagePath'] = img
#             with open(os.path.join(cur_belt, img.split('.')[0]+'.json'), 'w', encoding='utf-8') as f:
#                 json.dump(data, f, indent=4, ensure_ascii=False)


# # 根据图像大小进行筛选
# def remove_specific_categories(xml_file, categories):
#     # 以二进制模式读取文件内容
#     with open(xml_file, 'r', encoding='utf-8') as file:
#         file_content = file.read()
#     # 使用ElementTree从字符串解析XML
#     root = ET.fromstring(file_content)

#     # tree = ET.parse(xml_file)
#     # root = tree.getroot()
#     objects = root.findall('object')
#     for object in objects:
#         category = object.find('name').text
#         if category in categories:
#             root.remove(object)
    
#     # 将修改后的ET树转换为字符串
#     rough_string = ET.tostring(root, 'utf-8')
#     # 使用minidom解析这个字符串
#     reparsed = minidom.parseString(rough_string)
#     # 使用minidom的toprettyxml方法来获取格式化的字符串
#     pretty_string = reparsed.toprettyxml(indent="  ")
#     # 移除额外的空行
#     pretty_string_lines = pretty_string.splitlines()
#     pretty_string_no_blank_lines_or_declaration = "\n".join([line for line in pretty_string_lines if line.strip() != "" and not line.startswith('<?xml')])

#     # 将格式化的字符串写入原文件
#     with open(xml_file, 'w') as file:
#         file.write(pretty_string_no_blank_lines_or_declaration)

# # 源文件夹路径
# images_dir = '/data/bt/xray_gangsi/cls2_xray-gs_v0.1.2/images'  # 图像文件夹路径
# labels_dir = '/data/bt/xray_gangsi/cls2_xray-gs_v0.1.2/voc_labels'  # VOC标签文件夹路径

# # 目标文件夹路径
# large_images_dir = '/data/bt/xray_gangsi/LabeledData/20240301_concat/images'
# small_images_dir = '/data/bt/xray_gangsi/LabeledData/20240301/images'
# large_labels_dir = '/data/bt/xray_gangsi/LabeledData/20240301_concat/voc_labels'
# small_labels_dir = '/data/bt/xray_gangsi/LabeledData/20240301/voc_labels'

# # 定义要删除的类别
# categories_to_remove = ['jstart', 'jmiddle', 'jend']

# # 确保目标文件夹存在
# for directory in [large_images_dir, small_images_dir, large_labels_dir, small_labels_dir]:
#     if not os.path.exists(directory):
#         os.makedirs(directory)

# # 遍历图像文件夹
# for image_name in os.listdir(images_dir):
#     image_path = os.path.join(images_dir, image_name)
#     label_path = os.path.join(labels_dir, os.path.splitext(image_name)[0] + '.xml')  # 假设标签文件扩展名为.xml
    
#     # 首先处理标签文件，删除指定类别
#     if os.path.exists(label_path):
#         remove_specific_categories(label_path, categories_to_remove)

#     # 读取图像并获取宽度
#     image = cv2.imread(image_path)
#     height, width = image.shape[:2]
    
#     # 根据宽度分类
#     if width > 1500:
#         # 移动图像和标签到对应的大图像文件夹
#         shutil.copy(image_path, os.path.join(large_images_dir, image_name))
#         if os.path.exists(label_path):
#             shutil.copy(label_path, os.path.join(large_labels_dir, os.path.basename(label_path)))
#     else:
#         # 移动图像和标签到对应的小图像文件夹
#         shutil.copy(image_path, os.path.join(small_images_dir, image_name))
#         if os.path.exists(label_path):
#             shutil.copy(label_path, os.path.join(small_labels_dir, os.path.basename(label_path)))

# print("分类完成。")