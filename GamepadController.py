#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
import os
from DSJoyStick import DSJoyStick
from DSPlaySound import DSPlaySound
from Constants import *
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
