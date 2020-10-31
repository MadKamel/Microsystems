import filesystem, console, ram

def runFile(filename, RAM):

  E_RAM = ram.ram()

  E_RAM.writeTab('file', filesystem.readFile(filename))
  E_RAM.writeTab('type', filename.split('.')[1])
  
  if E_RAM.readTab('type') == 'dyn':
    E_RAM.writeTab('output', '')
    E_RAM.writeTab('split', E_RAM.readTab('file').split('%'))
    for i in range(len(E_RAM.readTab('split'))):
      if i/2 != int(i/2):
        if E_RAM.readTab('split')[i] == 'username':
          E_RAM.writeTab('output', E_RAM.readTab('output') + (RAM.readTab('user_name')))
      else:
        E_RAM.writeTab('output', E_RAM.readTab('output') + (E_RAM.readTab('split')[i]))
    console.writeline(E_RAM.readTab('output') + '\n')

  return E_RAM