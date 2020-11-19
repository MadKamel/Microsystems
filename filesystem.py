import os, system

def listCWD():
  return os.listdir()

def changeCWD(newDirectory):
  os.chdir(newDirectory)

def getCWD():
  return os.getcwd()

def readFile(file):
  return open(file).read()

def overwriteFile(file, data):
  open(file, '+w').write(data)

def appendFile(file, data):
  open(file, '+a').write(data)

def dumpError(data):
  overwriteFile(system.HROM.readTab('dumpfile'), str(data))