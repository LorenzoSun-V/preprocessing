import os
import json
from time import time
from glob import glob
import shutil


# 修改图片文件名、图片对应json文件名、json文件中的文件名
def rename(folder_path):
    # 遍历文件夹中的文件
    timestamp = int(time()*1000)
    for file_name in os.listdir(folder_path):
        # 检查文件是否为图片（根据需要调整条件）
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            base_name, extension = os.path.splitext(file_name)

            # 为图片和JSON生成新的文件名
            new_name = base_name + f"_{timestamp:13d}"
            new_image_name = new_name + extension  # 示例：原名_new.jpg
            new_json_name = new_name + ".json"
            
            # 构建完整的原始和新的文件路径
            original_image_path = os.path.join(folder_path, file_name)
            new_image_path = os.path.join(folder_path, new_image_name)
            original_json_path = os.path.join(folder_path, base_name + '.json')
            new_json_path = os.path.join(folder_path, new_json_name)
            
            # 修改图片文件名
            os.rename(original_image_path, new_image_path)
            
            # 如果对应的JSON文件存在，则读取并修改
            if os.path.exists(original_json_path):
                with open(original_json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 更新imagePath字段
                data['imagePath'] = new_image_name
                

                # 保存修改后的JSON数据到新文件名，并删除旧的JSON文件
                with open(new_json_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                os.remove(original_json_path)

    print("完成图片及其对应JSON文件的重命名和更新。")


# 将有目标的图片和没有目标的图片分开
def split_imgs(folder_path):
    folder = os.path.basename(folder_path)
    assert folder != '', "文件夹路径不能为空！"
    json_dirs = sorted(glob(os.path.join(folder_path, "*.json")))
    target_dir = os.path.join(os.path.dirname(folder_path), f"target_{folder}")

    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
    for json_dir in json_dirs:
        img_dir = json_dir.replace(".json", ".jpg")
        with open(json_dir, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if len(data['shapes']) > 0:
            os.system(f"cp {json_dir} {target_dir}")
            os.system(f"cp {img_dir} {target_dir}")
        # else:
        #     no_target_dir = os.path.join(folder_path, "no_target")
        #     if not os.path.exists(no_target_dir):
        #         os.makedirs(no_target_dir)
        #     os.system(f"mv {json_dir} {no_target_dir}")
        #     os.system(f"mv {img_dir} {no_target_dir}")


# 根据cls_name和数量选择目标图片
def select_target(folder_path, cls_name, num=1):
    json_dirs = sorted(glob(os.path.join(folder_path, "*.json")))
    target_dir = os.path.join(os.path.dirname(folder_path), f"select")

    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)

    num_dict = {}

    for json_dir in json_dirs:
        for cur_cls in cls_name:
            num_dict[cur_cls] = 0
        img_dir = json_dir.replace(".json", ".jpg")
        with open(json_dir, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if len(data['shapes']) > 0:
            for shape in data['shapes']:
                if shape['label'] in cls_name:
                    num_dict[shape['label']] += 1
        print(num_dict)
        if any(value >= num for value in num_dict.values()):
            shutil.copy(json_dir, target_dir)
            shutil.copy(img_dir, target_dir)


# 文件夹路径
# root_path = '/data/bt/xray_gangsi/LabeledData/zhoushan'
# folders = ['all_labeled']
# for folder in folders:
#     folder_path = os.path.join(root_path, folder)
#     split_imgs(folder_path)

# folder_path = '/data/bt/xray_gangsi/LabeledData/zhoushan/all'  # 将此路径替换为你的文件夹路径
# split_imgs(folder_path)

# 根据cls_name和数量选择目标图片  
folder_path = "/data/bt/xray_gangsi/LabeledData/zhoushan/20240315/images"
cls_name = ["fracture", "brokenlen"]
select_target(folder_path, cls_name, 2)