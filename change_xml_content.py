'''
Author: BTZN0325 sunjiahui@boton-tech.com
Date: 2023-11-29 13:24:24
LastEditors: BTZN0325 sunjiahui@boton-tech.com
LastEditTime: 2024-02-02 10:43:37
Description: 
'''
import xml.etree.ElementTree as ET
import os
import os.path as osp
from glob import glob


# 按条件修改xml文件里的类别
# def change_label(xml_file_path, output_dir):
#     tree = ET.parse(xml_file_path)
#     root = tree.getroot()

#     # 找到并修改<name>字段的内容
#     for obj in root.iter("object"):
#         name_element = obj.find("name")
#         if "embedding" in name_element.text:
#             name_element.text = "embedding"

#     # 保存修改后的XML文件
#     tree.write(output_dir)


# root = "/data/bt/xray_fanglun/LabeledData/20240229/voc_labels_old"
# output = "/data/bt/xray_fanglun/LabeledData/20240229/voc_labels"
# os.makedirs(output, exist_ok=True)
# xml_dirs = glob(os.path.join(root, "*.xml"))

# for xml_dir in xml_dirs:
#     file_name = os.path.basename(xml_dir)
#     output_dir = os.path.join(output, file_name)
#     change_label(xml_dir, output_dir)

#===========================================================================

# 删除xml文件的声明
# def remove_xml_declaration(file_path, out):
#     # 打开原始文件
#     with open(file_path, 'r', encoding='gbk') as file:
#         lines = file.readlines()
    
#     # 检查并移除第一行如果它是XML声明
#     if lines[0].startswith('<?xml'):
#         lines = lines[1:]
    
#     # 写入新文件或覆盖原始文件
#     with open(os.path.join(out, os.path.basename(file_path)), 'w') as file:
#         file.writelines(lines)

# input = "/data/bt/xray_gangsi/raw_zips/20240116_changjiu/长九/20240116_changjiu/voc_labels"
# out = "/data/bt/xray_gangsi/raw_zips/20240116_changjiu/长九/20240116_changjiu/voc_labels_new"
# if not os.path.exists(out):
#     os.makedirs(out, exist_ok=True)
# for i in glob(os.path.join(input, "*.xml")):
#     remove_xml_declaration(i, out)

#===========================================================================

# def modify_filename(xml_file_path, new_filename):
#     # 解析XML文件
#     tree = ET.parse(xml_file_path)
#     root = tree.getroot()

#     # 找到所有的<filename>标签并修改其内容
#     for filename_element in root.iter('filename'):
#         filename_element.text = new_filename

#     # 保存修改后的XML文件
#     tree.write(xml_file_path)

# xml_dirs = glob(osp.join("/data/bt/X-light-multi/cls5_xray_v0.2/voc_labels", "*.xml"))
# # 使用例子
# for xml_dir in xml_dirs:
#     file_name = f"{osp.basename(xml_dir)[:-4]}.jpg"
#     # new_filename = 'new_file_name.jpg'  # 替换成你想要设置的新文件名
#     modify_filename(xml_dir, file_name)

#===========================================================================

