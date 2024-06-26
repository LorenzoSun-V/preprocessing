'''
Author: BTZN0325 sunjiahui@boton-tech.com
Date: 2024-02-29 10:51:39
LastEditors: BTZN0325 sunjiahui@boton-tech.com
LastEditTime: 2024-03-22 15:09:05
Description: This is a profiler for measuring the performance of your code.

Usage:
	from profiler import Profiler

	with Profiler('my_function'):
		my_function()
	print(Profiler.get_avg_millis('my_function'))
'''
import time
from collections import Counter


class Profiler:
	__call_count   = Counter()
	__time_elapsed = Counter()

	def __init__(self, name, aggregate=False):
		self.name = name
		if not aggregate:
			Profiler.__call_count[self.name] += 1

	def __enter__(self):
		self.start = time.perf_counter()
		return self

	def __exit__(self, type, value, traceback):
		self.end = time.perf_counter()
		self.duration = self.end - self.start
		Profiler.__time_elapsed[self.name] += self.duration

	@classmethod
	def reset(cls):
		cls.__call_count.clear()
		cls.__time_elapsed.clear()

	@classmethod
	def get_avg_millis(cls, name):
		call_count = cls.__call_count[name]
		if call_count == 0:
			return 0
		return cls.__time_elapsed[name] * 1000 / call_count