'''
Author: BTZN0325 sunjiahui@boton-tech.com
Date: 2024-03-22 10:19:02
LastEditors: BTZN0325 sunjiahui@boton-tech.com
LastEditTime: 2024-03-22 15:13:15
Description: ImgSearcher for searching duplicated and similar images by perceptual hash.

hash_size:
    代表在计算图像的感知哈希（Perceptual Hash，pHash）时使用的哈希大小。
    直接影响到生成的哈希值的维度和精度，从而也影响到图像相似性比较的敏感度。
    hash_size的选择
    小的hash_size: 使用较小的哈希大小可以加快计算速度，并减少存储需求。然而，它可能会导致较高的假阳性率，即不相似的图像被错误地认为是相似的。
    大的hash_size: 使用较大的哈希大小可以提高哈希的唯一性和敏感性，从而减少假阳性率。但这也意味着计算和存储需求会增加，并且可能会增加对细微变化的敏感性，这在某些应用中可能不是期望的。
    因此，选择适当的hash_size是一种平衡，取决于具体应用中对速度、存储和精度的需求。
    在实际应用中，hash_size通常需要通过实验来确定，以找到最佳的平衡点。
    在图像搜索和去重的上下文中，常见的hash_size值范围是从8到16，这提供了合理的速度和准确度平衡。

Usage:
    python im_search.py --root_dir /path/to/root_dir --gc_dir /path/to/gc_dir --hash_size 8 --max_ham_distance 6
'''
import argparse
import os
import cv2
import glob
import shutil
from pathlib import Path
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from vptree import VPTree
import scipy.fftpack
import numpy as np
from profiler import Profiler


class ImgSearcher:
    def __init__(self, root_dir, gc_dir=None, hash_size=8, max_ham_distance=6, handle_dup=False, handle_similar=True, allowed_extensions=None, delete_img=True, parallel=True):
        self.root_dir = root_dir
        self.gc_dir = gc_dir if gc_dir else os.path.join(os.path.dirname(root_dir), 'gc_img')
        self.hash_size = hash_size
        self.max_ham_distance = max_ham_distance
        self.delete_img = delete_img
        if not delete_img and not os.path.exists(self.gc_dir):
            os.makedirs(self.gc_dir)
        self.handle_dup = handle_dup
        self.handle_similar = handle_similar
        self.parallel = parallel
        self.allowed_extensions = allowed_extensions if allowed_extensions else ['png', 'jpg', 'jpeg', 'JPG', 'PNG', 'JPEG']

    def find_dirs(self):
        folder = Path(self.root_dir)
        dirs = [str(folder / d) for d in sorted(os.listdir(folder)) if os.path.isdir(folder / d)]
        return dirs

    def find_files(self, dir_path):
        files = []
        for ext in self.allowed_extensions:
            files.extend(glob.glob(os.path.join(dir_path, f"*.{ext}")))
        return files
    
    def delete_file(self, file_path):
        if os.path.isfile(file_path):
            print(f"[INFO] Deleting file: {file_path}")
            os.remove(file_path)
        else:
            print(f"[WARNING] File not found for deletion: {file_path}")
    
    def move_file(self, file_path):
        if os.path.isfile(file_path):
            print(f"[INFO] Moving file: {file_path} to {self.gc_dir}")
            shutil.move(file_path, self.gc_dir)
        else:
            print(f"[WARNING] File not found for moving: {file_path}")

    def hash_img(self, img_path):
        hash_value = None
        try:
            hash_value = self.phash(img_path)
        except Exception as e:
            print(f"[Error] wrong img {img_path}: {e}")
        return hash_value

    def phash(self, img_path, highfreq_factor=4):
        """
        Perceptual Hash computation.
        Implementation follows
        http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html
        """
        img_size = self.hash_size * highfreq_factor
        image = cv2.imread(img_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (img_size, img_size))
        dct = scipy.fftpack.dct(scipy.fftpack.dct(resized, axis=0), axis=1)
        dctlowfreq = dct[:self.hash_size, :self.hash_size]
        med = np.median(dctlowfreq)
        diff = dctlowfreq > med
        hash_value = sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])
        return int(np.array(hash_value, dtype="float64"))

    def hamming_distance(self, a, b):
        return bin(int(a) ^ int(b)).count("1")

    def build_hash(self, img_paths):
        hashes = {}
        if self.parallel:
            with ThreadPoolExecutor() as e:
                hash_values = list(tqdm(e.map(self.hash_img, img_paths), total=len(img_paths)))
                for (hash_value, img_path) in zip(hash_values, img_paths):
                    hash_img_paths = hashes.get(hash_value, [])
                    hash_img_paths.append(img_path)
                    hashes[hash_value] = hash_img_paths
        else:
            loop = tqdm(enumerate(img_paths), total=len(img_paths))
            for (i, img_path) in loop:
                hash_value = self.hash_img(img_path)
                if hash_value is not None:
                    hash_img_paths = hashes.get(hash_value, [])
                    hash_img_paths.append(img_path)
                    hashes[hash_value] = hash_img_paths
        return hashes

    def build_tree(self, hashes):
        points = list(hashes.keys())
        tree = VPTree(points, self.hamming_distance)
        print("[INFO] build tree finished ")
        return tree
    
    def handle_dup_imgs(self, hashes):
        for hash_value, img_paths in hashes.items():
            if len(img_paths)>1:
                for idx,img_path in enumerate(img_paths):
                    if idx == 0: continue
                    if self.delete_img:
                        self.delete_file(img_path)
                    else:
                        self.move_file(img_path)

    def handle_similar_imgs(self, hashes):
        with Profiler('build_tree'):
            tree = self.build_tree(hashes)

        points = list(hashes.keys())
        for point in tqdm(points):
            results = tree.get_all_in_range(point, self.max_ham_distance)
            for (distance, hash_value) in sorted(results):
                if distance == 0: continue
                similar_img_paths = hashes.get(hash_value, [])
                if self.delete_img:
                    [self.delete_file(i) for i in similar_img_paths]
                else:
                    [self.move_file(i) for i in similar_img_paths]

    def handle_imgs(self, img_dir):
        old_img_paths = self.find_files(img_dir)
        print(f" [INFO] dir:{img_dir} [OLD] num: {len(old_img_paths)} ")

        with Profiler('build_hash'):
            hashes = self.build_hash(old_img_paths)
        
        if self.handle_dup:
            self.handle_dup_imgs(hashes)
        if self.handle_similar:
            self.handle_similar_imgs(hashes)

        new_img_paths = self.find_files(img_dir)
        print(f" [INFO] dir:{img_dir} [NEW] num: {len(new_img_paths)} ")
        print(f" [INFO] dir:{img_dir} [REMOVE] num: {len(old_img_paths) - len(new_img_paths)} \n")

    def run(self):
        img_dirs = self.find_dirs()
        if len(img_dirs) > 0:
            with ThreadPoolExecutor() as e:
                list(tqdm(e.map(self.handle_imgs, img_dirs), total=len(img_dirs)))
        else:
            self.handle_imgs(self.root_dir)
        
        print(f"build_hash_time:{Profiler.get_avg_millis('build_hash')}ms")
        print(f"build_tree_time:{Profiler.get_avg_millis('build_tree')}ms")


def parse_opt():
    parser = argparse.ArgumentParser(description="im search")
    parser.add_argument('root_dir', help='folder path of root_path')
    parser.add_argument('--gc_dir', default=None, help='folder path of garbage collection')
    parser.add_argument('--hash_size', type=int, default=8, help='hash size')
    parser.add_argument('--max_ham_distance', type=int, default=6, help='max hamming distance')
    parser.add_argument('--handle_dup', default=False, type=bool, help='handle duplicated img')
    parser.add_argument('--handle_similar', default=True, type=bool, help='handle similar img')
    parser.add_argument('--delete_img', action='store_true', help='delete img')
    parser.add_argument('--parallel', default=True, type=bool, help='parallel')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_opt()
    searcher = ImgSearcher(root_dir=args.root_dir,
                           gc_dir=args.gc_dir, 
                           hash_size=args.hash_size,
                           max_ham_distance=args.max_ham_distance, 
                           handle_dup=args.handle_dup,
                           handle_similar=args.handle_similar,
                           delete_img=args.delete_img, 
                           parallel=args.parallel)
    searcher.run()
