class rom:
  def __init__(self, content):
    self.internalMem = content

  def readTab(self, tabName):
    try:
      return self.internalMem.get(tabName)
    except:
      return -1