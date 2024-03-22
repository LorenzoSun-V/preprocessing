'''
Author: BTZN0325 sunjiahui@boton-tech.com
Date: 2024-03-20 11:24:11
LastEditors: BTZN0325 sunjiahui@boton-tech.com
LastEditTime: 2024-03-22 15:31:46
Description: 
'''
import os
import os.path as osp
from glob import glob
from tqdm import tqdm
import shutil


def save_val_imgs(val_txt, save_dir):
    if not osp.exists(save_dir): os.makedirs(save_dir, exist_ok=True)
    with open(val_txt, 'r') as f:
        val_imgs = [i.strip() for i in f.readlines()]
    for img in tqdm(val_imgs):
        img_name = osp.basename(img)
        save_dst = osp.join(save_dir, img_name)
        shutil.copy(img, save_dst)


root_path = "/data/bt/kjg_multi/cls2_kjg_v0.1.5"
val_txt = osp.join(root_path, "trainval", "val.txt")
save_dir = osp.join(root_path, "val_imgs")
save_val_imgs(val_txt, save_dir)
