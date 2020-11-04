import sys, system, console, filesystem

if __name__ == '__main__':

  while True:
    try:
      if system.HRAM.readTab('system_active'):
        system.start()
      else:
        if system.HRAM.readTab('system_restart'):
          system.HRAM.writeTab('system_active', True)
        else:
          break

    except KeyError as err:
      system.HRAM.writeTab('crash_dump', 'KEY_ERROR:\n' + str(err))
      system.HRAM.writeTab('crash', True)
      system.HRAM.writeTab('crash_fatal', False)
      filesystem.dumpError(sys.exc_info())

    except TypeError as err:
      system.HRAM.writeTab('crash_dump', 'TYPE_ERROR:\n' + str(err))
      system.HRAM.writeTab('crash', True)
      system.HRAM.writeTab('crash_fatal', False)
      filesystem.dumpError(sys.exc_info())


    except FileNotFoundError as err:
      system.HRAM.writeTab('crash_dump', 'FILE_NOT_FOUND_ERROR:\n' + str(err))
      system.HRAM.writeTab('crash', True)
      system.HRAM.writeTab('crash_fatal', False)


    except Exception as err:
      system.HRAM.writeTab('crash_dump', 'UNKNOWN_ERROR:\n' + str(err) + '\n\n\nthis could be a fatal error. your computer will shutdown now.')
      system.HRAM.writeTab('crash', True)
      system.HRAM.writeTab('crash_fatal', True)

  console.clear()
  exit()