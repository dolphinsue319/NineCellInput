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
		if array == [-1, 0]:
			return 1
		if array == [1, 0]:
			return 2
		if array == [0, -1]:
			return 3
		if array == [0, 1]:
			return 4
		if array == [-1, -1]:
			return 5
		if array == [-1, 1]:
			return 6
		if array == [1, -1]:
			return 7
		if array == [1, 1]:
			return 8
	def intFromRightDirections(self, directions):
		if directions == [0, 0, 0, 1]:
			return 1
		if directions == [0, 1, 0, 0]:
			return 2
		if directions == [1, 0, 0, 0]:
			return 3
		if directions == [0, 0, 1, 0]:
			return 4
		if directions == [1, 0, 0, 1]:
			return 5
		if directions == [0, 0, 1, 1]:
			return 6
		if directions == [1, 1, 0 ,0]:
			return 7
		if directions == [0, 1, 1, 0]:
			return 8
	def getOutputs(self, willChooseDirectionCallback, didChooseDirectionCallback, willChooseRightDirectionCallback, didChooseRightDirectionCallback, clickCallbak, rightClickCallback):
		"""
		第一個參數是當左搖桿碰到某個方向時觸發的 callback
		第二個參數是使用者釋放了左搖桿
		第三個參數是當右搖桿碰到某個方向時觸發的 callback
		第四個參數是使用者釋放了右搖桿
		第五個參數是左搖桿被按下了
		第六個參數是右搖桿被按下了
		"""
		out = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		leftFocus = [0, 0]
		leftFocusBuffer = [0, 0]
		rightFocus = [0, 0, 0, 0]
		rightFocusBuffer = [0, 0, 0, 0]
		leftClickBuffer = 0
		rightClickBuffer = 0
		
		while True:
			pygame.event.pump()
			time.sleep(0.1)
			it = 0
			#Read input from the two joysticks       
			for i in range(0, self.myJoyStick.get_numaxes()):
				out[it] = round(self.myJoyStick.get_axis(i))
				it+=1
			#Read input from buttons
			for i in range(0, self.myJoyStick.get_numbuttons()):
				out[it] = self.myJoyStick.get_button(i)
				it+=1
			leftFocus[0], leftFocus[1] = out[0], out[1]
			# out[5] 右邊的上
			# out[6] 右邊的右
			# out[7] 右邊的下
			# out[8] 右邊的左
			# out[16] 右邊被按下
			rightFocus[0], rightFocus[1], rightFocus[2], rightFocus[3] = out[5], out[6], out[7], out[8]
			
			if out[15] == 1 and leftClickBuffer == 0:
				leftClickBuffer = 1
				clickCallbak()
			# 這個判斷是為了避免按下按鈕的時間太長，持續觸發 clickCallback
			if out[15] == 0 and leftClickBuffer == 1:
				leftClickBuffer = 0
				
			if out[16] == 1 and rightClickBuffer == 0:
				rightClickBuffer = 1
				rightClickCallback()
			if out[16] == 0 and rightClickBuffer == 1:
				rightClickBuffer = 0
				
			if leftFocus != [0, 0]:
				if leftFocusBuffer != leftFocus:
					leftFocusBuffer = list(leftFocus)
					willChooseDirectionCallback(self.intFromArray(leftFocus))
			# 使用者放掉了搖桿
			if (leftFocus == [0, 0]) and (leftFocusBuffer != leftFocus):
				didChooseDirectionCallback(self.intFromArray(leftFocusBuffer))
				leftFocusBuffer = list(leftFocus)
			
			if rightFocus != [0, 0, 0, 0]:
				if rightFocusBuffer != rightFocus:
					rightFocusBuffer = list(rightFocus)
					willChooseRightDirectionCallback(self.intFromRightDirections(rightFocusBuffer))

			# 使用者放掉了搖桿
			if rightFocus == [0, 0, 0, 0]:
				if rightFocusBuffer != rightFocus:
					didChooseRightDirectionCallback(self.intFromRightDirections(rightFocusBuffer))
					rightFocusBuffer = list(rightFocus)
	#test
	def test(self):
		while True:
			print self.getOutputs()
