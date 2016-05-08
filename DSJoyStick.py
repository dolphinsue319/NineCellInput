#!/usr/bin/python
# -*- coding: utf-8 -*-

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
	
	def getOutputs(self):
		out = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		it = 0 #iterator
		pygame.event.pump()
			
		#Read input from the two joysticks       
		for i in range(0, self.myJoyStick.get_numaxes()):
			out[it] = round(self.myJoyStick.get_axis(i))
			it+=1
		#Read input from buttons
		for i in range(0, self.myJoyStick.get_numbuttons()):
			out[it] = self.myJoyStick.get_button(i)
			it+=1
		return out
	#test
	def test(self):
		while True:
			print self.getOutputs()
