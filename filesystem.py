import os, system, traceback

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
  overwriteFile(system.HROM.readTab('dumpfile'), str(data) + '\n' + str(traceback.extract_tb(data[2])))

def removeFile(path):
  if os.path.exists(path):
    os.remove(path)
    return True
  else:
    return False