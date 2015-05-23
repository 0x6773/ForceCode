#!/usr/bin/env python2

from __future__ import print_function
from bs4 import BeautifulSoup as bs
import requests
import sys
import os

def readConfig():
    """
    Read conf file and returns (editorName, pathToSave)
    """
    confPath = os.path.expanduser("~")
    confFile = os.path.join(confPath, ".forcecode")

    if not os.path.isfile(confFile):
        fileI = open(confFile, "w")
        fileI.write("editor:gedit:")
        fileI.write("path:~/.forceCode/:")
        fileI.close()
        return ('gedit','~/.forceCode/')

    else:
        file = open(confFile, "r")
        data = file.read()
        data = data.split(':')
        return (data[1], data[3])

class forcecode:
    """
    Class to extract information from CodeForces Website
    """
    def __init__(self):
        """
        Initializes the class
        """
        self.round = raw_input("Enter the round number : ")
        assert self.round.isdigit()
        self.url = r"http://codeforces.com/contest/" + str(self.round) + r"/problems"
        self.editor, self.tempPath = readConfig()

        print("Waiting to Connect to CodeForces...")
        self.soup = bs(requests.get(self.url).text)
        print("Round " + self.round + " Connected!")

        self.tmpPath = os.path.expanduser(os.path.join(self.tempPath + str(self.round)))

        self.data = [{}]
        self.input = []
        self.output = []

        self.doIt()

    def doIt(self):
        self.getIO()
        self.getQuestion()
        self.saveData()
        #bl.showAll()


    def getIO(self):
        """
        Parses input/output data from self.soup
        """
        di = self.soup.findAll('div',{'class' : 'input'})
        do = self.soup.findAll('div',{'class' : 'output'})

        for x, y in zip(di, do):
            t1 = str(x).replace("<div class=\"input\"><div class=\"title\">Input</div><pre>","")
            t1 = t1.replace("<br/>","\n").replace("</pre></div>","")
            t2 = str(y).replace("<div class=\"output\"><div class=\"title\">Output</div><pre>","")
            t2 = t2.replace("<br/>","\n").replace("</pre></div>","")

            self.input.append(t1)
            self.output.append(t2)

    def getQuestion(self):
        """
        Parses Question from self.soup
        """
        t1 = []
        for x in self.soup.findAll('div', {'class' : 'title'}):
            t1.append(x.text)

        currQues = -1

        while len(t1) > 0:
            if t1[0] == "Input":
                try:
                    try:
                        self.data[currQues]["input"].append(self.input[0])
                        self.data[currQues]["output"].append(self.output[0])
                    except:
                        self.data[currQues]["input"] = []
                        self.data[currQues]["output"] = []
                        self.data[currQues]["input"].append(self.input[0])
                        self.data[currQues]["output"].append(self.output[0])
                finally:
                    self.input.pop(0)
                    self.output.pop(0)
                    t1.pop(0)

            elif t1[0] == "Output":
                t1.pop(0)

            else:
                currQues += 1
                self.data[currQues]["question"] = t1[0]
                t1.pop(0)
                self.data.append({})

        self.data.pop()

        i = 0
        for t1 in self.soup.findAll('div', {'class' : 'problem-statement'}):
            full_quest = ""
            for quest in t1.findAll('p'):
                full_quest = full_quest + '\n' + quest.text
            self.data[i]["detail"] = full_quest
            i += 1

    def showAll(self):
        """
        Show All data on screen
        """
        for dat in self.data:
            print("Question : ")
            print(dat["question"])
            print(dat["detail"])
            print("Input : ")
            for x in dat["input"]:
                print(x)
            print("Output : ")
            for x in dat["output"]:
                print(x)
            raw_input("Press Any Key...")

    def saveData(self):
        """
        Save data to Disk
        """
        fileN = ""
        for tgn in xrange(len(self.data)):

            tg = chr(ord('A') + tgn)
            tagPath = os.path.join(self.tmpPath, tg)

            if not os.path.exists(tagPath):
                os.makedirs(tagPath)

            inputFile = os.path.join(tagPath, "input.txt")
            outputFile = os.path.join(tagPath, "output.txt")
            cppFile = os.path.join(tagPath, "program" + tg + ".cpp")

            fileI = open(inputFile, "w")
            for x in self.data[tgn]["input"]:
                try:
                    fileI.write(x)
                except:
                    fileI.write(x.encode('utf8'))
            fileI.close()

            fileO = open(outputFile, "w")
            for x in self.data[tgn]["output"]:
                try:
                    fileO.write(x)
                except:
                    fileO.write(x.encode('utf8'))
            fileO.close()

            fileC = open(cppFile, "w")
            fileC.write("/*\n")
            try:
                fileC.write(self.data[tgn]["question"])
            except:
                fileC.write(self.data[tgn]["question"].encode('utf8'))
            try:
                fileC.write(self.data[tgn]["detail"])
            except:
                fileC.write(self.data[tgn]["detail"].encode('utf8'))
            fileC.write("\n*/\n\n")

            fileC.close()

            fileN = fileN + " " + cppFile

        print("All files save to : " + self.tmpPath + ".")

        if self.editor != "NONE":
            print("Opening All files in " + self.editor + " editor.")
            os.system(self.editor + " " + fileN)

from glob import glob as globe

def getCppFile():
    """
    Returns the CPP file which is to be investigated
    """
    allCppFile = globe("*.cpp")
    if len(allCppFile) == 0 :
        print("No C++ File found.")
        sys.exit(1)
    elif len(allCppFile) > 1:
        print("More than one C++ files Found\nYou need to enter manually.")
        cppFile = raw_input("Enter the Name of C++ file : ")
        path = os.path.join(os.getcwd(), cppFile)
        if not os.path.isfile(path):
            print("No C++ File found with Name : " + cppFile)
            sys.exit(1)
        else:
            return os.path.join(os.getcwd(), cppFile)
    else:
        print("C++ file found : " + allCppFile[0])
        return os.path.join(os.getcwd(), allCppFile[0])

def getInputFile():
    """
    Returns the input file
    """
    inputFile = globe("input.txt")
    if len(inputFile) < 1:
        print("No input file found.\nEnter manually.")
        inputFile = raw_input("Enter input File : ")
        path = os.path.join(os.getcwd(), intputFile)
        if not os.path.isfile(path):
            print("No File found with Name : " + cppFile)
            sys.exit(1)
        else:
            return os.path.join(os.getcwd(), intputFile)
    else:
        print("Input File Found : " + inputFile[0])
        return os.path.join(os.getcwd(), inputFile[0])

def getOutputFile():
    """
    Returns the input file
    """
    outputFile = globe("output.txt")
    if len(outputFile) == 1:
        return os.path.join(os.getcwd(), outputFile[0])
class forcecoderunner:
    """
    Code to run the C++ file
    """
    def __init__(self):
        """
        Initialises the Class
        """
        self.cppFile = getCppFile()
        self.inputFile = getInputFile()
        self.outputOut = os.path.join(os.getcwd(), os.path.splitext(self.cppFile)[0] + ".out")

        self.command = "set -e;g++ -std=c++14 -Wall -Wextra -pedantic -pthread -O2 -Wshadow -Wformat=2 -Wfloat-equal -Wlogical-op -Wcast-qual -Wcast-align -fwhole-program -D_GLIBCXX_DEBUG -D_GLIBCXX_DEBUG_PEDANTIC "
        self.command = self.command + self.cppFile + " -o " + self.outputOut + " && " + self.outputOut + " < " + self.inputFile

        poutput = os.popen(self.command).read().strip()

        print("Output of your code : ")
        print(poutput)

        self.outputFile = getOutputFile()
        if not self.outputFile is None:
            file = open(self.outputFile, 'r')
            eoutput = file.read().strip()

            print("Currect Output : ")
            print(eoutput)
            if poutput == eoutput:
                try:
                    roundno = raw_input('Enter round number : ')
                    if roundno.isdigit():
                        os.system("xdg-open http://codeforces.com/contest/" + roundno + "/submit")
                except:
                    pass


if __name__ == '__main__':
    pass

if sys.argv[1] == '-r':
    f1 = forcecoderunner()

elif sys.argv[1] == '-h':
    getHelp()

else:
    bl = forcecode()
