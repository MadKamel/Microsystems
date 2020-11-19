import base64

def parsecmd(msg):
  cmd = None
  user = None
  spl = msg.split(' ')
  if spl[1] == 'PRIVMSG':
    user = spl[0][1:].split('!')[0]
    cmd = spl[3][1:].split('\r\n')[0]
  
  return cmd, user, ' '.join(spl[3:])[1:].split('\r\n')[0]

def encode_file(file):
  msg_proc = open(file).read().encode('ascii')
  msg_proc = base64.b64encode(msg_proc)
  msg_proc = msg_proc.decode('ascii')
  return msg_proc

def decode_file(file, data):
  wker = base64.b64decode(data).decode('utf-8')
  open(file, 'w+').write(wker)