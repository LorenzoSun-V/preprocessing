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
    label_dir = osp.join(dataset_dir, "labels")
    voc_dir = osp.join(dataset_dir, "Annotations")
    gt_dir = osp.join(dataset_dir, "gts")
    trainval_dir = osp.join(dataset_dir, "trainval")
    assert osp.exists(img_dir), f"{img_dir} is not existed!"
    assert osp.exists(label_dir), f"{label_dir} is not existed!"
    assert osp.exists(voc_dir), f"{voc_dir} is not existed!"
    assert osp.exists(gt_dir), f"{gt_dir} is not existed!"
    assert osp.exists(trainval_dir), f"{trainval_dir} is not existed!"
    assert osp.exists(osp.join(trainval_dir, "train.txt")), f"{trainval_dir}/train.txt is not existed!"
    assert osp.exists(osp.join(trainval_dir, "val.txt")), f"{trainval_dir}/val.txt is not existed!"
    return img_dir, label_dir, voc_dir, gt_dir, trainval_dir


def merge_dataset(dataset_dirs, dst_dir):
    if not osp.exists(dst_dir): os.makedirs(dst_dir, exist_ok=True)
    if not osp.exists(osp.join(dst_dir, "images")): os.makedirs(osp.join(dst_dir, "images"), exist_ok=True)
    if not osp.exists(osp.join(dst_dir, "labels")): os.makedirs(osp.join(dst_dir, "labels"), exist_ok=True)
    if not osp.exists(osp.join(dst_dir, "Annotations")): os.makedirs(osp.join(dst_dir, "Annotations"), exist_ok=True)
    if not osp.exists(osp.join(dst_dir, "gts")): os.makedirs(osp.join(dst_dir, "gts"), exist_ok=True)
    if not osp.exists(osp.join(dst_dir, "trainval")): os.makedirs(osp.join(dst_dir, "trainval"), exist_ok=True)

    train_img_list = []
    val_img_list = []

    for dataset_dir in dataset_dirs:
        img_dir, label_dir, voc_dir, gt_dir, trainval_dir = check_dirs(dataset_dir)

        # 使用 find 和 xargs 复制图片文件
        find_cmd = f"find {img_dir} -maxdepth 1 -print0 | xargs -0 cp -v -t {dst_dir}/images"
        print(find_cmd)
        os.system(find_cmd)

        # 使用 find 和 xargs 复制yolo标签文件
        find_cmd = f"find {label_dir} -maxdepth 1 -print0 | xargs -0 cp -v -t {dst_dir}/labels"
        print(find_cmd)
        os.system(find_cmd)

        # 使用 find 和 xargs 复制 XML 文件
        find_cmd = f"find {voc_dir} -maxdepth 1 -name '*.xml' -print0 | xargs -0 cp -v -t {dst_dir}/Annotations"
        print(find_cmd)
        os.system(find_cmd)

        # 使用 find 和 xargs 复制 GT 文件
        find_cmd = f"find {gt_dir} -maxdepth 1 -print0 | xargs -0 cp -v -t {dst_dir}/gts"
        print(find_cmd)
        os.system(find_cmd)

        # 读取 train.txt 和 val.txt 文件，将图片路径添加到 train_img_list 和 val_img_list 中
        with open(osp.join(trainval_dir, "train.txt"), "r") as f:
            for line in f:
                img_name = line.rsplit("/", 1)[-1]
                img_path = osp.join(dst_dir, "images", img_name)
                train_img_list.append(img_path)
            with open(osp.join(dst_dir, "trainval/train.txt"), "w") as f:
                f.writelines(train_img_list)
        
        with open(osp.join(trainval_dir, "val.txt"), "r") as f:
            for line in f:
                img_name = line.rsplit("/", 1)[-1]
                img_path = osp.join(dst_dir, "images", img_name)
                val_img_list.append(img_path)
            with open(osp.join(dst_dir, "trainval/val.txt"), "w") as f:
                f.writelines(val_img_list)

    print("merge done!")


dataset_dirs = [
    "/data/lorenzo/datasets/fire-smoke/fire/cls1_fire_v0.1",
    "/data/lorenzo/datasets/fire-smoke/fire/cls1_fire_v0.1.2",
]
dst_dir = "/data/lorenzo/datasets/fire-smoke/fire/cls1_fire_v0.1.3"
merge_dataset(dataset_dirs, dst_dir)

