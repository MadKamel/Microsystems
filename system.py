import console, ram, rom, misc, filesystem, exec, error, re

HRAM = ram.ram()
HROM = rom.rom({'user_list' : ['root'], 'pass_list' : ['toor'], 'sudo_list' : [True], 'dumpfile' : 'dump00.dmp', 'use_regexp' : ',', 'usefile' : 'users.use'})


HRAM.writeTab('host_name', 'microsystem')
HRAM.writeTab('system_active', True)
HRAM.writeTab('crash', False)
HRAM.writeTab('system_restart', False)

def start():
  console.clear()
  if HRAM.readTab('crash'):
    console.writeline('your microsystem computer has crashed. here is some info.')
    console.writeline(HRAM.readTab('crash_dump'))
    if HRAM.readTab('crash_fatal'):
      misc.delay(5000)
      console.writeline('shutting down now...')
      misc.delay(1000)
      HRAM.writeTab('system_active', False)
    else:
      HRAM.writeTab('crash', False)
      console.writeline('your computer will resume in 5 seconds.')
      misc.delay(5000)
      console.writeline('resuming your computer')
      misc.delay(1000)
  console.clear()
  console.writeline('welcome to microsystems.')
  console.writeline('')
  filesystem.changeCWD('/home/runner/Microsystems/home')

  RAM = ram.ram()
  RAM.purge()

  RAM.writeTab('usefile_content', open(HROM.readTab('usefile')).read().split('\n'))
  RAM.writeTab('sudo_list', re.split(HROM.readTab('use_regexp'), RAM.readTab('usefile_content')[0]) + HROM.readTab('sudo_list'))
  RAM.writeTab('user_list', re.split(HROM.readTab('use_regexp'), RAM.readTab('usefile_content')[1]) + HROM.readTab('user_list'))
  RAM.writeTab('pass_list', re.split(HROM.readTab('use_regexp'), RAM.readTab('usefile_content')[2]) + HROM.readTab('pass_list'))
  RAM.writeTab('user_session_active', False)

  while HRAM.readTab('system_active'):
    if not(RAM.readTab('user_session_active')):
      while not(RAM.readTab('user_session_active')):
        console.writeline('please log in.')
        RAM.writeTab('user_name', console.readline('  username: '))
        RAM.writeTab('pass_word', console.readline('  password: '))
        if RAM.readTab('user_name') in RAM.readTab('user_list') + HROM.readTab('user_list'):
          if RAM.readTab('pass_word') == RAM.readTab('pass_list')[RAM.readTab('user_list').index(RAM.readTab('user_name'))]:
            RAM.writeTab('user_session_active', True)
            RAM.writeTab('user_is_sudo', RAM.readTab('sudo_list')[RAM.readTab('user_list').index(RAM.readTab('user_name'))])
            console.clear()
          else:
            console.clear()
            console.writeline('error: password incorrect.')
            console.writeline('')
        else:
          console.clear()
          console.writeline('error: invalid user.')
          console.writeline('')


    RAM.writeTab('user_input', console.readline(RAM.readTab('user_name') + '@' + HRAM.readTab('host_name') + ' ~ $ '))

    if RAM.readTab('user_input') == 'restart':
      HRAM.writeTab('system_restart', True)
      HRAM.writeTab('system_active', False)

    elif RAM.readTab('user_input') == 'clear':
      console.clear()

    elif RAM.readTab('user_input') == 'ls':
      console.writeline('\nhere is the directory listing:')
      RAM.writeTab('tmp00', filesystem.listCWD())
      
      for i in range(len(RAM.readTab('tmp00'))):
        console.writeline('> ' + RAM.readTab('tmp00')[i])

      console.writeline('\n\nlisting complete\n')

    elif RAM.readTab('user_input')[:3] == 'cat':
      console.writeline('reading ' + RAM.readTab('user_input')[4:] + '...\n\n' + filesystem.readFile(RAM.readTab('user_input')[4:]) + '\n')
    
    elif RAM.readTab('user_input')[:3] == 'run':
      console.writeline('running ' + RAM.readTab('user_input')[4:] + '...\n')
      RAM.writeTab('last_exec', exec.runFile(RAM.readTab('user_input')[4:], RAM))
      
    elif RAM.readTab('user_input') == 'shutdown':
      HRAM.writeTab('system_restart', False)
      HRAM.writeTab('system_active', False)

    elif RAM.readTab('user_input') == 'dumpram':
      if RAM.readTab('user_is_sudo'):
        console.writeline(RAM.dumpAll())
      else:
        console.writeline('\nyou are not a super-user.')

    elif RAM.readTab('user_input') == 'dumphrom':
      if RAM.readTab('user_is_sudo'):
        console.writeline(HROM.dumpAll())
      else:
        console.writeline('\nyou are not a super-user.')

    elif RAM.readTab('user_input') == 'dumphram':
      if RAM.readTab('user_is_sudo'):
        console.writeline(HRAM.dumpAll())
      else:
        console.writeline('\nyou are not a super-user.')

    elif RAM.readTab('user_input') == 'dumperam':
      if RAM.readTab('user_is_sudo'):
        try:
          console.writeline(RAM.readTab('last_exec').dumpAll())
        except:
          pass
      else:
        console.writeline('\nyou are not a super-user.')

    elif RAM.readTab('user_input') == 'logout':
      RAM.writeTab('user_session_active', False)
      console.clear()

    elif RAM.readTab('user_input') == 'purgeram':
      if RAM.readTab('user_is_sudo'):
        console.writeline(RAM.purge())
      else:
        console.writeline('\nyou are not a super-user.')

    elif RAM.readTab('user_input') == 'fatalcrash':
      if RAM.readTab('user_is_sudo'):
        raise error.FatalTestException
      else:
        console.writeline('\nyou are not a super-user.')

    elif RAM.readTab('user_input') == 'crash':
      if RAM.readTab('user_is_sudo'):
        raise error.TestException
      else:
        console.writeline('\nyou are not a super-user.')