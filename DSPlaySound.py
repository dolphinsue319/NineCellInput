#!/usr/bin/python
# -*- coding: utf-8 -*-
import platform
from subprocess import call
import os
from GlobalVars import *

class DSPlaySound:
	"""
	為了讓這個產品能同時在 mac 及 RPi 上發出聲音，所以建立這個 class 用來播放音檔
	"""
	def __init__(self):
		self.OSMAC = 1
		self.OSRPI = 0
		self.os = self.OSMAC
		if "Darwin" not in platform.platform():
			print "This is RPi environment"
			self.os = self.OSRPI
			
	def play(self, path, isHint):
		print path
		if self.os == self.OSMAC:
			self.playSoundInMac(path, isHint)
		else:
			self.playSoundInRPi(path, isHint)
		
	def playWithArray(self, array, isHint):
		for char in array:
			path = os.path.dirname(os.path.abspath(__file__)) + u"/sounds/"+ char + u".wav"
			self.play(path, isHint)
		
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
		print "shouldSayHint is: " + str(shouldSayHint())
		if shouldSayHint() == False:
			return
		path = os.path.dirname(os.path.abspath(__file__)) + u"/documents/"+ filename + u".wav"
		if self.os == self.OSMAC:
			self.playSoundInMac(path, True)
		else:
			self.playSoundInRPi(path, True)

	def playSoundInMac(self, path, isHint):
		if isHint:
			call(["say", "-v", "Bells", "do"])
		else:
			call(["say", "-v", "Bells", "ding"])
		try:
			call(["afplay", path])
		except:
			print("afplay is failed, the file is: " + path)
		
	def playSoundInRPi(self, path, isHint):
		if isHint:
			call(["amixer", "cset", "numid=3", "1"])
		else:
			call(["amixer", "cset", "numid=3", "2"])
		try:
			call(["aplay", path])
		except:
			print "aplay is failed, the file is: " + path
