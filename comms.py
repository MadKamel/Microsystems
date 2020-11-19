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
  return base64.b64encode(open(file).read().encode('ascii')).decode()

def decode_file(file, data):
  wker = base64.b64decode(data).decode('utf-8')
  open(file, 'w').write(wker)