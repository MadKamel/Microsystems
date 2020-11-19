# taken from https://github.com/MadKamel/Irkbot-IRC-Bot
import socket


class IRC:

  irc = socket.socket()

  def __init__(self):  
    self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def send(self, msg):
    self.irc.send(("PRIVMSG " + self.chan + " :" + msg + "\n").encode('utf-8'))

  def connect(self, server, channel, botnick):
    self.chan = channel
    print("connecting to: " + server)
    self.irc.connect((server, 6667))
    print("connection complete.")

    self.irc.send(("USER " + botnick + " " + botnick + " " + botnick + " :(MadKamel) Irkbot\n").encode('utf-8'))
    self.irc.send(("NICK " + botnick + "\n").encode('utf-8'))
    self.irc.send(("JOIN " + channel + "\n").encode('utf-8'))
    print("IRC.connect() finished.")

  def get_text(self):
    text = self.irc.recv(2040).decode()
    if text.find('PING') != -1:
      self.irc.send(('PONG ' + text.split()[1] + '\r\n').encode('utf-8'))

    return text