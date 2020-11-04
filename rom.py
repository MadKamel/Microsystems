class rom:
  def __init__(self, content):
    self.internalMem = content

  def readTab(self, tabName):
    try:
      return self.internalMem.get(tabName)
    except:
      return -1

  def dumpAll(self):
    output = '\ntotal addresses: ' + str(len(self.internalMem))
    for item, amount in self.internalMem.items():
      output = output + '\n\t' + '{} ({})'.format(item, amount)
    return output + '\n\n'