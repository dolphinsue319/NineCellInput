#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
from subprocess import call
from DSJoyStick import DSJoyStick

kSymbols = {
    '11':u'ㄅ', '12':u'ㄆ', '13':u'ㄇ', '14':u'ㄈ', '15':u'ㄉ', '16':u'ㄊ', '17':u'ㄋ', '18':u'ㄌ',
        '21':u'ㄍ', '22':u'ㄎ', '23':u'ㄏ', '24':u'ㄐ', '25':u'ㄑ', '26':u'ㄒ',
        '31':u'ㄓ', '32':u'ㄔ', '33':u'ㄕ', '34':u'ㄖ', '35':u'ㄗ', '36':u'ㄘ', '37':u'ㄙ',
        '41':u'ㄧ', '42':u'ㄨ', '43':u'ㄩ',
        '51':u'ㄚ', '52':u'ㄛ', '53':u'ㄜ', '54':u'ㄝ', '55':u'ㄞ', '56':u'ㄟ', '57':u'ㄠ', '58':u'ㄡ',
        '61':u'ㄢ', '62':u'ㄣ', '63':u'ㄤ', '64':u'ㄥ', '65':u'ㄦ',
        '71':u'',  '72':u'ˊ',  '73':u'ˇ', '74':u'ˋ',  '75':u'˙'}
kHeadSymbols = [
                u"ㄅ", u"ㄆ", u"ㄇ", u"ㄈ",
                u"ㄉ", u"ㄊ", u"ㄋ", u"ㄌ",
                u"ㄍ", u"ㄎ", u"ㄏ",
                u"ㄐ", u"ㄑ", u"ㄒ",
                u"ㄓ", u"ㄔ", u"ㄕ", u"ㄖ",
                u"ㄗ", u"ㄘ", u"ㄙ"]
kBodySymbols = [u'ㄧ', u'ㄨ', u'ㄩ']
kFootSymbols = [
                u'ㄚ', u'ㄛ', u'ㄜ', u'ㄝ',
                u'ㄞ', u'ㄟ', u'ㄠ', u'ㄡ',
                u'ㄢ', u'ㄣ', u'ㄤ', u'ㄥ',
                u'ㄦ']

currentMode = 0
j = DSJoyStick()
oneNumber = 0
# 兩個 int 組成一個注音符號
twoNumbers = ""
aWord = ""
sentence = []
observing = False

def willSelectDirectionCallback(direction):
    print("willSelectDirectionCallback: " + str(direction))
def getDirectionCallback(direction):
    print("getDirectionCallback: " + str(direction))
def getClickCallback(click):
    print("getClickCallback: " + str(direction))

j.getOutputs(willSelectDirectionCallback, getDirectionCallback, getClickCallback)
#while True:
#	time.sleep(0.3)
#	outputs = j.getOutputs()
#	values[0] = outputs[0]
#	values[1] = outputs[1]
#	values[2] = outputs[15]
#	if currentMode == 0:
#		if (len([i for i in values if i <> 0]) > 0):
#			oneNumber = intFromArray(values)
#			observing = True
#
#		if (observing == True) and (values[0] == values[1] == values[2] == 0):
#			#這時要發出一個聲音提示她剛輸入的是哪個數字
#			print "one number is inputted: " + str(oneNumber)
#			observing = False
#			twoNumbers += str(oneNumber)
#			oneNumber = 0
#
#		if len(twoNumbers) == 2:
#			aSymbol = kSymbols.get(twoNumbers, 0)
#			print "symbol: " + aSymbol
#			if aSymbol != 0:
#				aWord += aSymbol
#				if twoNumbers[:1] == "7":
#					# 已輸入聲韻，表示這個中文字輸入完了
#					sentence.append(aWord)
#					print "sentence: " + ', '.join(sentence)
#					aWord = ""
#				else:
#					# 還沒輸入聲韻，這時要提示她輸入的是哪個注音符號
#					print "a symbol is inputted: " + aSymbol
#				twoNumbers = ""
#			else:
#				# 沒有這個注音符號
#				print("there is no this word")
#				twoNumbers = ""
#		if values[2] == 1:
#			observing = False
#			currentMode = 1
#	else:
#		print "entered menu mode"
#		if values[0] == -1:
#			# 刪除前一個輸入的東西
#			if oneNumber != 0:
#				print "a number is deleted: " + oneNumber
#				oneNumber = 0
#				currentMode = 0
#
#		if values[0] == 1:
#			# 依序發出句子裡每個字的聲音
#			for word in sentence:
#				path = u"sounds/"+ word + u".wav"
#				print "play sound: " + path
#				call(["afplay", path])
#			sentence = []
#			currentMode = 0
#			
#		
