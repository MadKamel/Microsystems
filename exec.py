import filesystem, console, ram, re

def runFile(filename, RAM):

  E_RAM = ram.ram()

  E_RAM.writeTab('file', filesystem.readFile(filename))
  E_RAM.writeTab('type', filename.split('.')[1])
  
  if E_RAM.readTab('type') == 'dyn':
    E_RAM.writeTab('write_on', True)
    E_RAM.writeTab('tmp00', [''])
    E_RAM.writeTab('output', '')
    E_RAM.writeTab('split', E_RAM.readTab('file').split('%'))
    for i in range(len(E_RAM.readTab('split'))):
      if i/2 != int(i/2):
        if E_RAM.readTab('split')[i] == 'username':
          E_RAM.writeTab('output', E_RAM.readTab('output') + (RAM.readTab('user_name')))
        elif E_RAM.readTab('split')[i] == 'issudo':
          E_RAM.writeTab('output', E_RAM.readTab('output') + (RAM.readTab('user_is_sudo')))
      else:
        E_RAM.writeTab('output', E_RAM.readTab('output') + (E_RAM.readTab('split')[i]))
    E_RAM.writeTab('split2', re.split('<|>', E_RAM.readTab('output')))
    for i in range(len(E_RAM.readTab('split2'))):
      console.writeline(E_RAM.readTab('split2')[i])

  return E_RAM