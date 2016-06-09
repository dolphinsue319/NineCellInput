#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
import os
import unittest
import inspect
from DSJoyStick import DSJoyStick
from DSPlaySound import DSPlaySound
from Constants import *
from subprocess import call

j = DSJoyStick()
playsound = DSPlaySound()
# 兩個 int 組成一個注音符號
twoNumbers = ""
# 2~4 個 symbol 組成一個字
aWord = ""
# 一個句子
sentence = []
# 口頭禪群組ID
mantraID = []

def willChooseDirectionCallback(direction):
    """
    左搖桿被移到某一個方向了，且還沒放掉搖桿
    """
    print inspect.stack()[0][3] + ': ' + str(direction)
    
def didChooseDirectionCallback(direction):
    """
    左搖桿從某個方向被放掉了。
    """
    print inspect.stack()[0][3] + ': ' + str(direction)
    global twoNumbers
    global aWord
    if currentMode == kModeFreeSpeak or currentMode == kModeMantraAdd:
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
    print inspect.stack()[0][3]
    
def willChooseRightDirectionCallback(direction):
    print inspect.stack()[0][3] + ': ' + str(direction)
    
def didChooseRightDirectionCallback(direction):
    print inspect.stack()[0][3] + ': '+ str(direction)
    global currentMode
    if currentMode == kModeMenu:
        # 進入了選單模式
        if direction == 1:
            currentMode = kModeFreeSpeak
            print "choosed free speak mode"
        if direction == 2:
            currentMode = kModeMantra
            print "choosed mantra mode"
            """
            1. 選擇是要建立、刪除還是選擇，右搖桿的 1 為建立， 2 為選擇，3為刪除。並提示使用者：您正要[建立, 刪除, 選擇]口頭禪，請先選擇群組
            2. 選擇口頭禪群組並提示使用者目前選擇的是哪一個群組(您選擇的群組是：xy)
            """
        if direction == 8:
            currentMode = kModeDocument
            print "choosed document mode"
        return
            
    if currentMode == kModeFreeSpeak or currentMode == kModeMantraAdd:
        global twoNumbers
        global aWord
        global sentence
        if direction == 1:
            deletePreviousInput()
        if direction == 2:
            if currentMode == kModeFreeSpeak:
                # 依序發出句子裡每個字的聲音
                playCurrentSentence()
            if currentMode == kModeMantraAdd:
                ss = ','.join(sentence) + '\n'
                filename = os.path.dirname(os.path.abspath(__file__)) + '/mantra/' + ''.join(map(str, mantraID)) + '.txt'
                if os.path.isfile(filename) == False:
                    call(['touch', filename])
                f = open(filename, 'a')
                f.write(ss.encode('utf8'))
                f.close()
                print("write a sentence to file")
            sentence = []
        if direction == 3:
            # 預聽目前為止輸入的句子，所以最後不清除 sentence
            playCurrentSentence()
        return

    if currentMode == kModeMantra:
        if len(mantraID) < 2:
            # 輸入口頭禪群組
            print "enter mantraID"
            mantraID.append(direction)
            if len(mantraID) == 2:
                print("enter mantra group: " + ''.join(map(str, mantraID)))
                currentMode = kModeMantraAdd
        return

def playCurrentSentence():
    print inspect.stack()[0][3]
    for word in sentence:
        path = os.path.dirname(os.path.abspath(__file__)) + u"/sounds/"+ word + u".wav"
        print "play sound: " + path
        playsound.play(path)

def playHint(message):
    print inspect.stack()[0][3]
    print "play message: " + ', '.join(message)
    for word in message:
        path = os.path.dirname(os.path.abspath(__file__)) + u"/sounds/"+ word + u".wav"
        playsound.play(path)

def deletePreviousInput():
    """
    在 currentMode 為 0 時，右搖桿向左要刪除前一個輸入的數字、前一個注音符號、前一個字
    """
    print inspect.stack()[0][3]
    global twoNumbers
    global aWord
    global sentence
    if len(twoNumbers) == 1:
        print("delete one number: " + str(twoNumbers))
        twoNumbers = ""
    elif len(aWord) > 0:
        print("delete final symbol in a word: " + aWord[-1])
        aWord = aWord[:-1]
    elif len(sentence) > 0:
        print("delete final word in sentence: " + sentence[-1])
        sentence = sentence[:-1]
        
def getRightClickCallback():
    print inspect.stack()[0][3]
    global currentMode
    currentMode = kModeMenu
    # 進到 menu 時，清除剛剛輸入的任何字元
    global twoNumbers
    global aWord
    global sentence
    twoNumbers = ""
    aWord = ""
    sentence = []
    print "enter mode menu"
    
j.getOutputs(willChooseDirectionCallback, 
didChooseDirectionCallback, 
willChooseRightDirectionCallback, 
didChooseRightDirectionCallback, 
getClickCallback, 
getRightClickCallback)

class tests(unittest.TestCase):
    def test_hint():
        playHint(HintMessages.enterMenuMode)
#unittest.main()