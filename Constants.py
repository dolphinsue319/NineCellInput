#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

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

class HintMessages:
	"""
	這個 class 用來放提示如何使用這個系統的語句，這些字串可以用這個網站轉: http://crptransfer.moe.gov.tw
	"""
	enterMenuMode = ['ㄋㄧㄣˊ','ㄐㄧㄣˋ','ㄖㄨ˙','ㄌㄜ','ㄒㄩㄢˇ', 'ㄉㄢ', 'ㄇㄛˊ', 'ㄕˋ']

# 自由輸入模式
kModeFreeSpeak = 1
kModeMantra = 2
kModeMantraActionUnassigned = 20
kModeMantraAdd = 21
kModeMantraSelect = 22
kModeMantraDelete = 23
kModeMantraIndexChoosing = 24
kModeMantraIndexChoosed = 25
kModeDocument = 8
# 選單模式
kModeMenu = 0
kModeSetupEnvironment = 7

class HintMessagesTest(unittest.TestCase):
	def test_is_message_array(self):
		message = HintMessages.enterMenuMode
		self.assertIsInstance(message, list)
		
#unittest.main()