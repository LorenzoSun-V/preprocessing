import os
import os.path as osp


duplicate_num = 10
train_extra = "train_extra.txt"
train_extra_list = []
train_extra_stem_list = []
with open("1.txt", 'r') as f:
    duplicate_img_dirs = [i.strip() for i in f.readlines()]
    for img_dir in duplicate_img_dirs:
        img_name_ori = osp.basename(img_dir)
        img_name = osp.basename(img_name_ori).rsplit('.', 1)[0]
        img_dirname = osp.dirname(img_dir)
        root_path = osp.dirname(img_dirname)
        voc_label_dirname = osp.join(root_path, "voc_labels")
        txt_label_dirname = osp.join(root_path, "labels")
        assert osp.exists(voc_label_dirname), f"{voc_label_dirname} is not existed!"
        ext = img_name_ori.rsplit('.', 1)[-1]

        for i in range(duplicate_num):
            new_img_name = f"{img_name}_{i}.{ext}"
            print(new_img_name)
            new_img_dir = osp.join(img_dirname, new_img_name)
            os.system(f"cp {img_dir} {new_img_dir}")
            train_extra_list.append(f"{new_img_dir}\n")
            train_extra_stem_list.append(f"{new_img_name.rsplit('.', 1)[0]}\n")
            print(f"cp {img_dir} {new_img_dir}")

            new_voc_label_dir = osp.join(voc_label_dirname, f"{new_img_name.rsplit('.', 1)[0]}.xml")
            os.system(f"cp {osp.join(voc_label_dirname, f'{img_name}.xml')} {new_voc_label_dir}")
            print(f"cp {osp.join(voc_label_dirname, f'{img_name}.xml')} {new_voc_label_dir}")

            new_txt_label_dir = osp.join(txt_label_dirname, f"{new_img_name.rsplit('.', 1)[0]}.txt")
            os.system(f"cp {osp.join(txt_label_dirname, f'{img_name}.txt')} {new_txt_label_dir}")
            print(f"cp {osp.join(txt_label_dirname, f'{img_name}.txt')} {new_txt_label_dir}")
    
    with open(train_extra, 'w') as f_out:
        f_out.writelines(train_extra_list)
    
    with open("train_extra_stem.txt", 'w') as f_out:
        f_out.writelines(train_extra_stem_list)