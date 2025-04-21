import os
import cv2
import json
import numpy as np
import re


# ==== 配置区 ====
root_dir    = '/data/nofar/temp/output'       # 存放各个子视频文件夹的根目录
output_root = '/data/nofar/temp/demo'      # 合成后的视频存放目录
fps         = 5              # 输出视频帧率
# =================

def natural_key(fname):
    # 假设文件名格式为 <prefix>_<num>.jpg
    base = os.path.splitext(fname)[0]
    # 找到最后一段数字
    m = re.search(r'(\d+)$', base)
    return int(m.group(1)) if m else base


os.makedirs(output_root, exist_ok=True)

for sub in sorted(os.listdir(root_dir)):
    folder = os.path.join(root_dir, sub)
    if not os.path.isdir(folder):
        continue

    # 找出所有 JPG
    imgs = sorted(
        [f for f in os.listdir(folder) if f.lower().endswith('.jpg')],
        key=natural_key)
    
    if not imgs:
        print(f"跳过 {sub}：目录中无 jpg 文件")
        continue

    # 读取第一帧，获取尺寸
    sample = cv2.imread(os.path.join(folder, imgs[0]))
    h, w = sample.shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_path = os.path.join(output_root, f"{sub}.mp4")
    writer = cv2.VideoWriter(out_path, fourcc, fps, (w, h))

    for img_name in imgs:
        img_path = os.path.join(folder, img_name)
        img = cv2.imread(img_path)
        if img is None:
            continue

        # 加载同名 JSON
        base = os.path.splitext(img_name)[0]
        jpath = os.path.join(folder, base + '.json')
        if os.path.isfile(jpath):
            with open(jpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for shape in data.get('shapes', []):
                pts = np.array(shape['points'], dtype=np.int32)
                label = shape.get('label', '')
                cv2.polylines(img, [pts], True, (0,0,255), 2)
                x0, y0 = pts[0]
                cv2.putText(
                    img, label,
                    (int(x0), int(max(y0-10,0))),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                    (0,0,255), 2, cv2.LINE_AA
                )

        writer.write(img)

    writer.release()
    print(f"✅ 已生成：{out_path}")
