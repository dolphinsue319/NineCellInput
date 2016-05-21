#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import pygame
class DSJoyStick:
	"""
	用來接收所有的搖桿事件
	"""
	def __init__(self):
		pygame.init()
		joyStickCount = pygame.joystick.get_count()
		if joyStickCount == 0:
			return nil
		self.myJoyStick = pygame.joystick.Joystick(0)
		self.myJoyStick.init()
		print self.myJoyStick.get_name()
		return 
	def intFromArray(self, array):
		"""
		給我一個兩個整數的 array，這個 func 會依照九宮格回傳一個 Int 回去。http://nine-cells-input.herokuapp.com/input
		"""
		if array[0] == 0:
			if array[1] < 0:
				return 3
			if array[1] > 0:
				return 4
		if array[0] < 0:
			if array[1] == 0:
				return 1
			if array[1] < 0:
				return 5
			if array[1] > 0:
				return 6
		if array[0] > 0:
			if array[1] == 0:
				return 2
			if array[1] < 0:
				return 7
			if array[1] > 0:
				return 8

	def getOutputs(self, willTouchDirectionCallback, didChooseDirectionCallback, clickCallbak):
		"""
		第一個參數是當搖桿碰到某個方向時觸發的 callback
		第二個參數是使用者釋放了該方向的搖桿
		第三個參數是使用者按下了搖桿
		"""
		out = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		leftFocus = [0, 0, 0]
		leftFocusBuffer = [0, 0]
		
		while True:
			pygame.event.pump()
			time.sleep(0.3)
			it = 0
			#Read input from the two joysticks       
			for i in range(0, self.myJoyStick.get_numaxes()):
				out[it] = round(self.myJoyStick.get_axis(i))
				it+=1
			#Read input from buttons
			for i in range(0, self.myJoyStick.get_numbuttons()):
				out[it] = self.myJoyStick.get_button(i)
				it+=1
			leftFocus[0], leftFocus[1], leftFocus[2] = out[0], out[1], out[15]
#			print(out)
			if leftFocus[2] == 1:
				clickCallbak()
			if leftFocus[0] != 0 or leftFocus[1] != 0:
				if leftFocus[0] != leftFocusBuffer[0] or leftFocus[1] != leftFocusBuffer[1]:
					leftFocusBuffer[0] = leftFocus[0]
					leftFocusBuffer[1] = leftFocus[1]
					willTouchDirectionCallback(self.intFromArray(leftFocus))
			# 使用者放掉了搖桿
			if (leftFocus[0] == 0 and leftFocus[1] == 0) and (leftFocusBuffer[0] != 0 or leftFocusBuffer[1] != 0):
				didChooseDirectionCallback(self.intFromArray(leftFocusBuffer))
				leftFocusBuffer = [0, 0]

	#test
	def test(self):
		while True:
			print self.getOutputs()
