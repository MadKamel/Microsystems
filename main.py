import system, console

if __name__ == '__main__':

  while True:
    if system.HRAM.readTab('system_active'):
      system.start()
    else:
      if system.HRAM.readTab('system_restart'):
        system.HRAM.writeTab('system_active', True)
      else:
        break



  console.clear()
  exit()