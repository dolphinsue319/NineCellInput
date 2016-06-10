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
mantraGroupID = []
# 口頭禪序號
mantraIndex = []

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
    print inspect.stack()[0][3] + ': ' + str(direction)
    global currentMode
    global mantraGroupID
                        
    if currentMode in [kModeFreeSpeak, kModeMantraAdd] and len(mantraGroupID) == 2:
        inputSentence(direction)
        return
    if currentMode == kModeMantraSelect and len(mantraGroupID) == 2:
        inputMantraIndex(direction)
        print "selecting a mantra to say"
        return
        
    if currentMode == kModeMenu:
        selectMode(direction)
        return
        
    if currentMode == kModeMantraActionUnassigned:
        # 進入了口頭禪模式，現在要選擇是要建立、選擇還是刪除口頭禪
        if direction == 1:
            currentMode = kModeMantraAdd
            print "enter add mantra mode"
        if direction == 2:
            currentMode = kModeMantraSelect
            print "enter select mantra mode"
        if direction == 3:
            currentMode = kModeMantraDelete
            print "enter delete mantra mode"
        return

    if currentMode in [kModeMantraAdd, kModeMantraSelect, kModeMantraDelete]:
        if len(mantraGroupID) < 2:
            # 輸入口頭禪群組
            print "input mantraGroupID"
            mantraGroupID.append(direction)
            if len(mantraGroupID) == 2:
                if currentMode in [kModeMantraSelect, kModeMantraDelete]:
                    # "選擇及刪除"口頭禪前，先檢查該群組是不是已存在了
                    if os.path.isfile(mantraGroupIDFilePath()) == False:
                        print "there is no sucu mantraGroupID, should input one more time."
                        mantraGroupID = []
                        return
                print("enter mantra group: " + ''.join(map(str, mantraGroupID)))
                
def mantraGroupIDFilePath():
    """
    將 mantraGroupID 這個 array 轉成檔案路徑傳回去
    """
    global mantraGroupID
    return os.path.dirname(os.path.abspath(__file__)) + '/mantra/' + ''.join(map(str, mantraGroupID)) + '.txt'
    
def inputMantraIndex(direction):
    """
    輸入口頭禪序號，輸入完用按下右鍵表示結束輸入。
    """
    print inspect.stack()[0][3]
    global mantraIndex 
    mantraIndex.append(direction)
    currentMode = kModeMenu

def sayMantra(index):
    print inspect.stack()[0][3]
    index = index - 1
    f = open(mantraGroupIDFilePath(), 'r')
    for i in range(0, index - 1, 1):
        f.readline()
    print f.readline()

def selectMode(direction):
    """
    這裡是 menu mode，選擇要進何種模式：1為自由說話，2為口頭禪，3為說明模式
    """
    print inspect.stack()[0][3]
    global currentMode
    if direction == 1:
        currentMode = kModeFreeSpeak
        print "enter free speak mode"
    if direction == 2:
        currentMode = kModeMantraActionUnassigned
        print "choosing mantra action"
    if direction == 8:
        currentMode = kModeDocument
        print "enter document mode"
        

def playCurrentSentence():
    """
    輸出一段話
    """
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
    """
    右搖桿被按下去了
    """
    print inspect.stack()[0][3]
    global currentMode
    if currentMode == kModeMantraSelect:
        index = ''.join(map(str, mantraIndex ))
        print "the mantra index is: " + index
        sayMantra(int(index))
        return
    currentMode = kModeMenu
    # 進到 menu 時，清除剛剛輸入的任何字元
    global twoNumbers
    global aWord
    global sentence
    global mantraGroupID
    twoNumbers = ""
    aWord = ""
    sentence = []
    mantraGroupID = []
    print "enter mode menu"
    
def inputSentence(direction):
    print inspect.stack()[0][3]
    global twoNumbers
    global aWord
    global sentence
    global currentMode
    global mantraGroupID
    if direction == 1:
        deletePreviousInput()
    if direction == 2:
        if currentMode == kModeFreeSpeak:
            # 依序發出句子裡每個字的聲音
            playCurrentSentence()
        if currentMode == kModeMantraAdd:
            ss = ','.join(sentence) + '\n'
            filename = os.path.dirname(os.path.abspath(__file__)) + '/mantra/' + ''.join(map(str, mantraGroupID)) + '.txt'
            if os.path.isfile(filename) == False:
                call(['touch', filename])
            f = open(filename, 'a')
            f.write(ss.encode('utf8'))
            f.close()
            currentMode = kModeMenu
            mantraGroupID = []
            print("write a sentence to file")
        sentence = []
    if direction == 3:
        # 預聽目前為止輸入的句子，所以最後不清除 sentence
        playCurrentSentence()

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