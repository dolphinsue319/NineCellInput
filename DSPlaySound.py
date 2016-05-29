#!/usr/bin/python
# -*- coding: utf-8 -*-
import platform
from subprocess import call

class DSPlaySound:
	"""
	為了讓這個產品能同時在 mac 及 RPi 上發出聲音，所以建立這個 class 用來播放音檔
	"""
	def __init__(self):
		self.os = 0
		if "Darwin" not in platform.platform():
			self.os = 1
	def play(self, path):
		if self.os == 0:
			call(["afplay", path])
		else:
			call(["aplay", path])
		