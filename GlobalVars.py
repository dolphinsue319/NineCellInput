#!/usr/bin/python
# -*- coding: utf-8 -*-

def shouldSayHint():
	f = open('shouldSayHint', 'r')
	value = f.readline()
	f.close()
	return value == 'True'
	
def updateShouldSayHint():
	oldValue = shouldSayHint()
	f = open('shouldSayHint', 'w')
	if oldValue == True:
		f.write('False')
	else:
		f.write('True')
	f.close()