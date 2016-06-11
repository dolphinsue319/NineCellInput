#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
import os
import unittest
import inspect
import codecs
from DSJoyStick import DSJoyStick
from DSPlaySound import DSPlaySound
from Constants import *
from subprocess import call

j = DSJoyStick()
playsound = DSPlaySound()
currentMode = kModeMenu
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
# 是不是正要刪除一句口頭禪
mantraDeleting = False

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
                        
    if currentMode == kModeFreeSpeak:
        inputSentence(direction)
        return
    if currentMode == kModeMantraAdd and len(mantraGroupID) == 2:
        inputSentence(direction)
        return
    if currentMode in [kModeMantraSelect, kModeMantraDelete] and len(mantraGroupID) == 2:
        inputMantraIndex(direction)
        print "selecting a mantra index to say"
        return
        
    if currentMode == kModeMenu:
        selectMode(direction)
        return
        
    if currentMode == kModeMantraIndexChoosing:
        # 使用者正在選擇口頭禪的序號
        if direction == 1:
            index = mantraIndexAdd(-1)
            sayMantra(index)
            return
        if direction == 2:
            index = mantraIndexAdd(1)
            sayMantra(index)
            return
        print("Back to menu mode, because input other numbers")
        enterModeMenu()
        return
            
    if currentMode == kModeMantraActionUnassigned:
        # 進入了口頭禪模式，現在選擇了是要建立、選擇還是刪除口頭禪
        selectMantraMode(direction)
        print "please input 2 digits mantra group ID"
        return

    if currentMode in [kModeMantraAdd, kModeMantraSelect, kModeMantraDelete]:
        if len(mantraGroupID) < 2:
            # 輸入口頭禪群組
            print "please input mantraGroupID"
            mantraGroupID.append(direction)
            if len(mantraGroupID) == 2:
                print("enter mantra group: " + ''.join(map(str, mantraGroupID)))
                if currentMode in [kModeMantraSelect, kModeMantraDelete]:
                    # "選擇及刪除"口頭禪前，先檢查該群組是不是已存在了
                    if os.path.isfile(mantraGroupIDFilePath()) == False:
                        print "there is no sucu mantraGroupID, you should input it again."
                        mantraGroupID = []
                        return
                    print("Please enter mantra index")

def mantraIndexAdd(addValue):
    print inspect.stack()[0][3] + " the add value is: " + str(addValue)
    global mantraIndex
    indexInt = int(''.join(map(str, mantraIndex)))
    indexInt += addValue
    if indexInt < 2:
        indexInt = 1
    indexStr = str(indexInt)
    mantraIndex = []
    for char in indexStr:
        mantraIndex.append(char)
    return indexInt
    
def selectMantraMode(direction):
    # 進入了口頭禪模式，現在要選擇是要建立、選擇還是刪除口頭禪
    global currentMode
    if direction == 1:
        currentMode = kModeMantraAdd
        print "enter add mantra mode"
    if direction == 2:
        currentMode = kModeMantraSelect
        global mantraIndex
        mantraIndex = []
        print "enter select mantra mode"
    if direction == 3:
        currentMode = kModeMantraDelete
        global mantraDeleting
        mantraDeleting = True
        print "enter delete mantra mode"

                
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

def sayMantra(index):
    """
    提示或說一句口頭禪
    """
    print inspect.stack()[0][3] + ", the index is: " + str(index)
    f = codecs.open(mantraGroupIDFilePath(), 'r', 'utf-8')
    index = index - 1
    global sentence
    global mantraIndex
    global currentMode
    for i in range(0, index, 1):
        thisLine = f.readline()
    sentence = f.readline().rstrip('\n').split(',')
    if ''.join(sentence) == '':
        print "The index of mantra is not exist, please input again"
        mantraIndex = []
        currentMode = kModeMantraSelect
        return

    global mantraDeleting
    if currentMode == kModeMantraIndexChoosing:
        if mantraDeleting == True:
            print "Do you want to delete: \"" + ''.join(sentence) + "\""
        else:
            print "Do you want to say: \"" + ''.join(sentence) + "\""
        return
    if currentMode == kModeMantraIndexChoosed:
        if mantraDeleting == True:
            deleteMantra(index)
        else:
            playCurrentSentence()
        enterModeMenu()
    
def deleteMantra(index):
    print inspect.stack()[0][3] + ', the index is: ' + str(index)
    f = open(mantraGroupIDFilePath(), "r")
    lines = f.readlines()
    f.close()
    lines.pop(index)
    f = open(mantraGroupIDFilePath(), "w")
    for line in lines:
        f.write(line)
    f.close()
    global mantraDeleting
    mantraDeleting = False
    
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
        print "please choose mantra action"
    if direction == 8:
        currentMode = kModeDocument
        print "enter document mode"
        

def playCurrentSentence():
    """
    輸出一段話
    """
    print inspect.stack()[0][3]
    global sentence
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
    global mantraIndex
    if currentMode in [kModeMantraSelect, kModeMantraDelete] and len(mantraIndex) > 0:
        currentMode = kModeMantraIndexChoosing
        index = ''.join(map(str, mantraIndex))
        print "preview a mantra, the index is: " + index
        sayMantra(int(index))
        return
    if currentMode == kModeMantraIndexChoosing:
        currentMode = kModeMantraIndexChoosed
        index = ''.join(map(str, mantraIndex))
        print "the mantra index is: " + index
        sayMantra(int(index))
        return
    enterModeMenu()
    
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
            print("write a sentence to file")
            enterModeMenu()
        sentence = []
    if direction == 3:
        # 預聽目前為止輸入的句子，所以最後不清除 sentence
        playCurrentSentence()

def enterModeMenu():
    """
    進入選單模式
    """
    print inspect.stack()[0][3]
    global currentMode
    global twoNumbers
    global aWord
    global sentence
    global mantraGroupID
    global mantraIndex
    currentMode = kModeMenu
    mantraGroupID = []
    twoNumbers = ""
    aWord = ""
    sentence = []
    mantraIndex = []


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