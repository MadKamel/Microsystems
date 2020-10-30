import filesystem, console, ram

def runFile(filename):

  E_RAM = ram.ram()

  E_RAM.writeTab('file', filesystem.readFile(filename))
  E_RAM.writeTab('type', filename.split('.')[1])
  
  console.writeline()
  return E_RAM