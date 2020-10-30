class ram:
  def __init__(self):
    self.internalMem = {}

  def readTab(self, tabName):
    try:
      return self.internalMem.get(tabName)
    except:
      return -1

  def writeTab(self, tabName, data=None):
    try:
      self.internalMem[tabName] = data
      return 0
    except:
      return -1

  def dumpAll(self):
    output = '\ntotal addresses: ' + str(len(self.internalMem))
    for item, amount in self.internalMem.items():
      output = output + '\n\t' + '{} ({})'.format(item, amount)
    return output + '\n\n'

  def purge(self):
    self.internalMem = {}