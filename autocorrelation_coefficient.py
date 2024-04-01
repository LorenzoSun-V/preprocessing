'''
Author: BTZN0325 sunjiahui@boton-tech.com
Date: 2024-03-29 16:32:53
LastEditors: BTZN0325 sunjiahui@boton-tech.com
LastEditTime: 2024-04-01 13:45:27
Description: autocorrelation coefficient(自相关系数)计算，用于判断图像中的前后列/行是否相似，自相关系数趋近于1则相似度越高
'''
import argparse
import os.path as osp
import cv2
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from copy import deepcopy
from tqdm import tqdm


class AutocorrelationCoefficient:
    def __init__(self, gray_pics, filter_width=20):
        """
        Args:
            gray_pics: list, the list of grayscale images(or img path)
        """
        assert isinstance(gray_pics, list), 'gray_pics should be a list'
        self.img_dirs = []
        if isinstance(gray_pics[0], str):
            self.img_dirs = deepcopy(gray_pics)
            pics = [cv2.imread(pic) for pic in self.img_dirs]
            gray_pics = [cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY) for pic in pics]
        self.gray_pics = gray_pics
        self.filter_width = filter_width

    def cal_autocorrelation_coefficient_pic(self, pic_gray):
        co = np.ones(pic_gray.shape[1])
        for cols in range(1, pic_gray.shape[1]):
            A = pic_gray[:, cols-1].astype('float')
            A_mean = A.mean()
            B = pic_gray[:, cols].astype('float')
            B_mean = B.mean()
            co[cols] = np.dot(A-A_mean, B-B_mean) / np.sqrt(np.sum((A-A_mean)**2) * np.sum((B-B_mean)**2))

        # Apply a minimum filter to the correlation values,用于平滑曲线
        co_min_filt = np.ones(pic_gray.shape[1])
        for cols in range(self.filter_width, pic_gray.shape[1]):
            co_min_filt[cols] = np.min(co[(cols-self.filter_width+1):cols+1])
        return co, co_min_filt
    
    def cal_autocorrelation_coefficient_pics(self, if_plot=True):
        co_list = []
        co_min_filt_list = []
        for index, pic_gray in tqdm(enumerate(self.gray_pics)):
            co, co_min_filt = self.cal_autocorrelation_coefficient_pic(pic_gray)
            co_list.append(co)
            co_min_filt_list.append(co_min_filt)
            if if_plot:
                self.plot_autocorrelation_coefficient_pic(co, co_min_filt, pic_gray.shape, index)
        return co_list, co_min_filt_list
    
    def plot_autocorrelation_coefficient_pic(self, co, co_min_filt, shape, index):
        # Plot the original grayscale image
        plt.figure()

        # Plot the correlation and the filtered correlation values
        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.plot(co)
        plt.axis([0, shape[1], 0, 1])
        plt.title('Correlation Coefficients')
        plt.grid(True)

        plt.subplot(2, 1, 2)
        plt.plot(co_min_filt)
        plt.axis([0, shape[1], 0, 1])
        plt.title('Filtered Correlation Coefficients')
        plt.grid(True)
        if len(self.img_dirs) > 0:
            plt.savefig(osp.join(osp.dirname(self.img_dirs[index]), f'{osp.splitext(osp.basename(self.img_dirs[index]))[0]}.png'))
        else:
            plt.savefig(f'{index}.png')


def opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('img_dir', type=str, help='The directory of images')
    parser.add_argument('--filter_width', type=int, default=20, help='The width of the filter')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = opt()
    autocc = AutocorrelationCoefficient(glob(osp.join(args.img_dir, '*.jpg')), args.filter_width)
    autocc.cal_autocorrelation_coefficient_pics()