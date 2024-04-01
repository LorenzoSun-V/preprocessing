'''
Author: BTZN0325 sunjiahui@boton-tech.com
Date: 2024-03-07 10:53:05
LastEditors: BTZN0325 sunjiahui@boton-tech.com
LastEditTime: 2024-03-29 14:22:07
Description: 
'''
import os
import os.path as osp


def check_dirs(dataset_dir):
    assert osp.exists(dataset_dir), f"{dataset_dir} is not existed!"
    img_dir = osp.join(dataset_dir, "images")
    voc_dir = osp.join(dataset_dir, "voc_labels")
    assert osp.exists(img_dir), f"{img_dir} is not existed!"
    assert osp.exists(voc_dir), f"{voc_dir} is not existed!"
    return img_dir, voc_dir

# 将多个数据集合并，形成一个新的数据集到dst_dir下
def merge_dataset(dataset_dirs, dst_dir):
    if not osp.exists(dst_dir): os.makedirs(dst_dir, exist_ok=True)
    if not osp.exists(osp.join(dst_dir, "images")): os.makedirs(osp.join(dst_dir, "images"), exist_ok=True)
    if not osp.exists(osp.join(dst_dir, "voc_labels")): os.makedirs(osp.join(dst_dir, "voc_labels"), exist_ok=True)
    for dataset_dir in dataset_dirs:
        img_dir, voc_dir = check_dirs(dataset_dir)
        cp_cmd = f"cp {img_dir}/*.jpg {dst_dir}/images"
        print(cp_cmd)
        os.system(cp_cmd)
        cp_cmd = f"cp {voc_dir}/*.xml {dst_dir}/voc_labels"
        print(cp_cmd)
        os.system(cp_cmd)
    print("merge done!")


dataset_dirs = [
    "/data/bt/kjg_multi/raw/new/yongfeng/20240325_yongfeng",
    "/data/bt/kjg_multi/raw/new/xinyegang/20240327_xinyegang",
    "/data/bt/kjg_multi/cls2_kjg_v0.1.5",
]
dst_dir = "/data/bt/kjg_multi/cls2_kjg_v0.1.6"
merge_dataset(dataset_dirs, dst_dir)

