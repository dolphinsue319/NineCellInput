#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
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
	
	def getOutputs(self, directionCallback, clickCallbak):
		out = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		focus = [0, 0, 0]
		it = 0 #iterator
		pygame.event.pump()

		while True:
			time.sleep(0.3)
			#Read input from the two joysticks       
			for i in range(0, self.myJoyStick.get_numaxes()):
				out[it] = round(self.myJoyStick.get_axis(i))
				it+=1
			#Read input from buttons
			for i in range(0, self.myJoyStick.get_numbuttons()):
				out[it] = self.myJoyStick.get_button(i)
				it+=1
			focus[0], focus[1], focus[2] = out[0], out[1], out[15]
						

	#test
	def test(self):
		while True:
			print self.getOutputs()
