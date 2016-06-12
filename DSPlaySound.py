#!/usr/bin/python
# -*- coding: utf-8 -*-
import platform
from subprocess import call
import os

class DSPlaySound:
	"""
	為了讓這個產品能同時在 mac 及 RPi 上發出聲音，所以建立這個 class 用來播放音檔
	"""
	def __init__(self):
		self.OSMAC = 1
		self.OSRPI = 0
		self.os = self.OSMAC
		if "Darwin" not in platform.platform():
			self.os = self.OSRPI
			
	def play(self, path):
		if self.os == self.OSMAC:
			self.playSoundInMac(path)
		else:
			call(["aplay", path])
			
	def playDoc(self, filename):
		"""
		給我文件的主檔名就好
		"""
		path = os.path.dirname(os.path.abspath(__file__)) + u"/documents/"+ filename + u".wav"
		if self.os == self.OSMAC:
			self.playSoundInMac(path)
		else:
			call(["aplay", path])

	def playSoundInMac(self, path):
		call(["say", "-v", "Bells", "dong", "dong"])
		call(["afplay", path])
