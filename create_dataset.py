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
    "/data/bt/xray_gangsi/cls4_xray-gs-sub_v0.1",
    "/data/bt/xray_gangsi/LabeledData/liyang/20240321",
    # "/data/bt/xray_gangsi/LabeledData/20240307",
]
dst_dir = "/data/bt/xray_gangsi/cls4_xray-gs-sub_v0.1.2"
merge_dataset(dataset_dirs, dst_dir)

