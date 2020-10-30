import os

def listCWD():
  return os.listdir()

def changeCWD(newDirectory):
  os.chdir(newDirectory)