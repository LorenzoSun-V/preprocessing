import os
import os.path as osp
from glob import glob
from tqdm import tqdm
import cv2


# 将拼接后的图像拆开
def split_img(img_path, save_path, hw):
    img_dirs = sorted(glob(osp.join(img_path, "*.jpg")))
    for img_dir in tqdm(img_dirs):
        img_name = osp.basename(img_dir)
        img = cv2.imread(img_dir)
        h, w = img.shape[:2]
        h_num = h//hw[0]
        w_num = w//hw[1]
        for i in range(h_num):
            for j in range(w_num):
                img_crop = img[i*hw[0]:(i+1)*hw[0], j*hw[1]:(j+1)*hw[1]]
                save_dir = osp.join(save_path, img_name.replace(".jpg", f"_{i}_{j}.jpg"))
                cv2.imwrite(save_dir, img_crop)


# 根据接头位置信息，查找前后的非接头图片（通过时间）
def find_target(joint_path, all_path):
    n = 3
    joints = sorted(glob(osp.join(joint_path, "*.jpg")))
    alls = sorted(glob(osp.join(all_path, "*.jpg")))
    alls_name = [osp.splitext(osp.basename(all))[0] for all in alls]
    for joint in tqdm(joints):
        joint_name = osp.basename(joint)
        joint_begin = joint_name.split("_")[0]
        joint_end = joint_name.split("_")[1]
        begin_index = alls_name.index(joint_begin)
        end_index = alls_name.index(joint_end)
        for i in range(begin_index-n, begin_index):
            os.system(f"cp {alls[i]} {joint_path}")

        for j in range(end_index+1, end_index+n+1):
            os.system(f"cp {alls[j]} {joint_path}")


if __name__ == "__main__":
    # n = 3
    img_path = "/home/sysadmin/lorenzo/deploy/LorenzoDeploy/fd/image/fl/20240315/big"
    save_path = "/home/sysadmin/lorenzo/deploy/LorenzoDeploy/fd/image/fl/20240315/small"
    hw = (1920, 1024)
    split_img(img_path, save_path, hw)

    # joint_path = "/lorenzo/deploy/LorenzoDeploy/fd/image/fl/20240315/big"
    # all_path = "/lorenzo/deploy/LorenzoDeploy/fd/image/fl/20240315/small"
    # find_target(joint_path, all_path)