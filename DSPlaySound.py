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
			
	def play(self, path, isHint):
		if self.os == self.OSMAC:
			self.playSoundInMac(path, isHint)
		else:
			self.playSoundInRPi(path, isHint)

	def playNumber(self, number):
		path = os.path.dirname(os.path.abspath(__file__)) + u"/documents/num"+ str(number) + u".wav"
		if self.os == self.OSMAC:
			self.playSoundInMac(path, True)
		else:
			self.playSoundInRPi(path, True)

	def playDoc(self, filename):
		"""
		給我文件的主檔名就好
		"""
		path = os.path.dirname(os.path.abspath(__file__)) + u"/documents/"+ filename + u".wav"
		if self.os == self.OSMAC:
			self.playSoundInMac(path, True)
		else:
			self.playSoundInRPi(path, True)

	def playSoundInMac(self, path, isHint):
		if isHint:
			call(["say", "-v", "Bells", "do", "do"])
		else:
			call(["say", "-v", "Bells", "ding", "ding"])
		call(["afplay", path])
		
	def playSoundInRPi(self, path, isHint):
		position = 'local'
		if isHint == False:
			position = 'hdmi'
		call(["omxplayer", "-o", position, path])