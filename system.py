import console, ram, rom, misc, filesystem, exec, error, re, irc, comms, time, threading, sys

HRAM = ram.ram()
HROM = rom.rom({'user_list' : ['root'], 'pass_list' : ['toor'], 'sudo_list' : ['True'], 'dumpfile' : 'sys/dump00.dmp', 'use_regexp' : ',', 'usefile' : 'sys/users.use', 'rootdir' : filesystem.getCWD(), 'server' : 'irc.freenode.net', 'channel' : '#mk-comms', 'inbox_dest' : 'sys/inbox/'})


HRAM.writeTab('host_name', 'micro1337')
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
      console.writeline('resuming your session...')
      misc.delay(1000)
    else:
      HRAM.writeTab('crash', False)
      console.writeline('your computer will resume in 5 seconds.')
      misc.delay(5000)
      console.writeline('resuming your computer')
      misc.delay(1000)
  console.clear()

  

  console.writeline('welcome to microsystems.')
  console.writeline('')

  filesystem.changeCWD(HROM.readTab('rootdir') + '/home/')


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
            # If user's sudo status is the string 'True' then they get sudo privs.
            RAM.writeTab('user_is_sudo', 'True' == RAM.readTab('sudo_list')[RAM.readTab('user_list').index(RAM.readTab('user_name'))])
            console.clear()
          else:
            console.clear()
            console.writeline('error: password incorrect.')
            console.writeline('')

          client = irc.IRC()
          RAM.writeTab('irc_name', RAM.readTab('user_name') + '-' + HRAM.readTab('host_name'))
          client.connect(HROM.readTab('server'), HROM.readTab('channel'), RAM.readTab('irc_name'),  "A Microsystems User")
          console.writeline('starting IRC listening daemon...')
          
          def ircListener(client):
            try:
              console.writeline('IRC listening daemon active.')
              while True:
                cmd, user, fullmsg = comms.parsecmd(client.get_text())
                if not cmd == None:
                  if cmd == 'ping':
                    client.send('pong')

                  elif cmd == 'pong':
                    RAM.writeTab('ponged', user)
                
                  elif cmd == 'send':
                    if fullmsg.split(' ')[1] == RAM.readTab('irc_name'):
                      sent_command = ' '.join(fullmsg.split(' ')[2:])
                      filesystem.appendFile(HROM.readTab('inbox_dest') + RAM.readTab('user_name') + '.inb', '[' + user + '] sent: ' + sent_command + '\n')

                  elif cmd == 'give':
                    if fullmsg.split(' ')[1] == RAM.readTab('irc_name'):
                      sent_command = ' '.join(fullmsg.split(' ')[2:])
                      if sent_command == 'ack':
                        RAM.writeTab('ack', True)
                      else:
                        RAM.writeTab('response', sent_command)
                        if sent_command.split(' ')[0] == 'file':
                          comms.decode_file(sent_command.split(' ')[1], ' '.join(sent_command.split(' ')[2:]))

                  elif cmd == 'rqst':
                    if fullmsg.split(' ')[1] == RAM.readTab('irc_name'):
                      rqst_data = ' '.join(fullmsg.split(' ')[2:])
                      if rqst_data == 'ack':
                        client.send('give ' + user + ' ack')
                      else:
                        client.send('fail ' + user + ' 0:RQST_NOT_RECOGNIZED')
                
                  elif cmd == 'fail':
                    if fullmsg.split(' ')[1] == RAM.readTab('irc_name'):
                      sent_command = ' '.join(fullmsg.split(' ')[2:])
                      RAM.writeTab('failed_msg', sent_command)
                      RAM.writeTab('failed_rqst', True)

            except Exception as e:
              console.writeline('\n\nIRC daemon died!')
              filesystem.dumpError(sys.exc_info())
              console.writeline(str(e) + '\n')
              #ircListeningDaemon = threading.Thread(target=ircListener, args=([client]), daemon=True)
              #ircListeningDaemon.start()

          ircListeningDaemon = threading.Thread(target=ircListener, args=([client]), daemon=True)
          ircListeningDaemon.start()

          console.writeline('IRC listening daemon set up.')

          console.writeline('microsystems MK-COMMS system set up.\n')
        else:
          console.clear()
          console.writeline('error: invalid user.')
          console.writeline('')


    RAM.writeTab('user_input', console.readline(RAM.readTab('user_name') + '@' + HRAM.readTab('host_name') + ' ~ $ '))

    if RAM.readTab('user_input') == 'restart':
      HRAM.writeTab('system_restart', True)
      HRAM.writeTab('system_active', False)

    elif RAM.readTab('user_input') == 'mk-ping':
      RAM.writeTab('ponged', '')
      client.send('ping')
      console.writeline('ping sent; listening for reply.')

      timer_start = time.time()
      while timer_start - time.time() > -1:
        if RAM.readTab('ponged') != '':
          console.writeline('user [' + RAM.readTab('ponged') + '] ponged.')
          RAM.writeTab('ponged', '')

      console.writeline('ping complete.\n')
    
    elif RAM.readTab('user_input').split(' ')[0] == 'mk-rqst':
      RAM.writeTab('ack', False)
      client.send('rqst ' + RAM.readTab('user_input').split(' ')[1] + ' ack')
      console.writeline('sending ack request..')
      timer_start = time.time()
      while timer_start - time.time() > -1:
        if RAM.readTab('ack'):
          break
      
      if RAM.readTab('ack'):
        console.writeline('ack request answered, continuing.')
        RAM.writeTab('response', '')
        RAM.writeTab('failed_rqst', False)
        client.send('rqst ' + RAM.readTab('user_input').split(' ')[1] + ' ' + ' '.join(RAM.readTab('user_input').split(' ')[2:]))
        timer_start = time.time()
        while timer_start - time.time() > -1:
          if '' != RAM.readTab('response'):
            console.writeline('got a response!')
            break
          
          elif RAM.readTab('failed_rqst'):
            console.writeline('request failed: ' + RAM.readTab('failed_msg'))
            break

      else:
        console.writeline('ack request ignored, aborting.')
        continue
      console.writeline('')



    elif RAM.readTab('user_input') == 'clear':
      console.clear()

    elif RAM.readTab('user_input').split(' ')[0] == 'del':
      if filesystem.removeFile(RAM.readTab('user_input').split(' ')[1]):
        console.writeline('file deleted successfully.')
      else:
        console.writeline('"' + RAM.readTab('user_input').split(' ')[1] + '" is not a valid file.')

    elif RAM.readTab('user_input') == 'ls':
      console.writeline('\nhere is the directory listing:')
      RAM.writeTab('tmp00', filesystem.listCWD())
      
      for i in range(len(RAM.readTab('tmp00'))):
        console.writeline('> ' + RAM.readTab('tmp00')[i])

      console.writeline('\n\nlisting complete\n')

    elif RAM.readTab('user_input')[:3] == 'cat':
      console.writeline('reading ' + RAM.readTab('user_input')[4:] + '...\n\n' + filesystem.readFile(RAM.readTab('user_input')[4:]) + '\n')
    
    elif RAM.readTab('user_input') == 'inbox':
      inbox = open(HROM.readTab('inbox_dest') + RAM.readTab('user_name') + '.inb').read().split('\n')
      for i in range(len(inbox)):
        console.writeline(inbox[i] + '\n')

    elif RAM.readTab('user_input') == 'clearinbox':
      open(HROM.readTab('inbox_dest') + RAM.readTab('user_name') + '.inb', 'w+').write('')
    
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

    elif RAM.readTab('user_input') == 'lastdump':
      if RAM.readTab('user_is_sudo'):
        console.writeline(open(HROM.readTab('dumpfile')).read())
      else:
        console.writeline('\nyou are not a super-user.')