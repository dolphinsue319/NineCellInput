#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
import os
from DSJoyStick import DSJoyStick
from DSPlaySound import DSPlaySound

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
# 自由輸入模式
kModeFreeSpeak = 1
kModeInputFavorite = 2
# 選單模式
kModeMenu = 0
currentMode = kModeFreeSpeak

j = DSJoyStick()
# 兩個 int 組成一個注音符號
twoNumbers = ""
# 2~4 個 symbol 組成一個字
aWord = ""
sentence = []
observing = False

def willChooseDirectionCallback(direction):
    """
    搖桿被移到某一個方向了，且還沒放掉搖桿
    """
    print("willSelectDirectionCallback: " + str(direction))
    
def didChooseDirectionCallback(direction):
    """
    搖桿從某個方向被放掉了。
    """
    print("getDirectionCallback: " + str(direction))
    global twoNumbers
    global aWord
    if currentMode == kModeFreeSpeak:
        twoNumbers += str(direction)
        if len(twoNumbers) < 2:
            print("one number entered: " + str(twoNumbers))
        else:
            # 使用者輸入了兩個數字，在這裡組成一個注音符號
            aSymbol = kSymbols.get(twoNumbers, 0)
            if aSymbol == 0:
                #TODO: 出聲提示使用者輸入錯誤
                print("this symble is not exist: " + twoNumbers)
                twoNumbers = twoNumbers[:-1]
                return
                
            print("a symbol is entered: " + aSymbol)
            aWord += aSymbol
            aSymbol = ""
            if twoNumbers[:1] == "7":
                # 當輸入聲韻，表示一個字輸入完了
                print("a word is entered: " + aWord)
                sentence.append(aWord)
                aWord = ""
                print("sentence is entered: " + str(sentence))
            twoNumbers = ""
    
def getClickCallback():
    print("getClickCallback")
    
def willChooseRightDirectionCallback(direction):
    print("willChooseRightDirectionCallback: " + str(direction))
    
def didChooseRightDirectionCallback(direction):
    print("didChooseRightDirectionCallback: " + str(direction))
    global currentMode
    if currentMode == kModeFreeSpeak:
        global twoNumbers
        global aWord
        global sentence
        if direction == 1:
            # 在 currentMode 為 0 時，右搖桿向左要刪除前一個輸入的數字、前一個注音符號、前一個字
            if len(twoNumbers) == 1:
                print("delete one number: " + str(twoNumbers))
                twoNumbers = ""
            elif len(aWord) > 0:
                print("delete final symbol in a word: " + aWord[-1])
                aWord = aWord[:-1]
            elif len(sentence) > 0:
                print("delete final word in sentence: " + sentence[-1])
                sentence = sentence[:-1]
        if direction == 2:
            # 依序發出句子裡每個字的聲音
            playCurrentSentence()
            sentence = []
        if direction == 3:
            # 預聽目前為止輸入的句子，所以最後不清除 sentence
            playCurrentSentence()
    if currentMode == kModeMenu:
        # 進入了選單模式
        if direction == 1:
            currentMode = kModeFreeSpeak
        if direction == 2:
            currentMode = kModeInputFavorite
            
def playCurrentSentence():
    playsound = DSPlaySound()
    for word in sentence:
        path = os.path.dirname(os.path.abspath(__file__)) + u"/sounds/"+ word + u".wav"
        print "play sound: " + path
        playsound.play(path)
            
    
def getRightClickCallback():
    print("getRightClickCallback")
    currentMode = kModeMenu
    
j.getOutputs(willChooseDirectionCallback, didChooseDirectionCallback, willChooseRightDirectionCallback, didChooseRightDirectionCallback, getClickCallback, getRightClickCallback)
