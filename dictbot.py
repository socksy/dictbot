from twisted.words.protocols import irc
from twisted.internet import protocol, reactor
import requests
import re
from bs4 import BeautifulSoup


def get_translation(word, direction):
    if direction is None:
        undecided = True
        direction = "ende"
    else:
        undecided = False

    #using the widget for a simple usage
    payload = { 'ddict': direction, 'search': word,
             'h': '200', 'w': '200'}
    r = requests.post("http://en.bab.la/widgets/dict.php", data=payload)

    soup = BeautifulSoup(r.text)
    if (not undecided) and (direction == "deen"):
        results = soup.find_all('td', {'class': 'lang2'})
    elif not undecided:
        results = soup.find_all('td', {'class': 'lang2'})
    else:
        results = soup.find_all('td', {'class': 'lang1'})
        results += soup.find_all('td', {'class': 'lang2'})

    if not results:
        return '[no translation found for '+str(word)+']'

    words = []
    for word in results:
        #whichever words are in strong are the ones searched for
        if word.div.a.strong is None:
            words.append(word.div.a.text)
    return ', '.join(words)

class TranslateBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        self.join('##deutsch')
        self.join('##deutsch-bot')

    def privmsg(self, user, channel, raw_msg):
        if raw_msg[0] == '!' or re.match("^.?"+self.nickname, raw_msg) != None:
            msg = re.sub(self.nickname + "[:,]? ?", '', raw_msg)
            print msg
            if msg.startswith('!de'):
                direction = "deen"
            elif msg.startswith('!en'):
                direction = "ende"
            else:
                direction = None
            msgsplit = msg.split(' ')
            if len(msgsplit) == 1:
                translatable = msgsplit[0].replace('!','')
            else:
                translatable = msgsplit[1]

            self.msg(channel, get_translation(translatable, direction).encode('utf-8'))

    def joined(self, channel):
        print ("Joined " +channel)

class TranslateBotFactory(protocol.ClientFactory):
    protocol = TranslateBot
    def __init__(self, nickname="dictbot"):
        self.nickname = nickname
    def clientConnectionLost(self, connector, reason):
        connector.connect()
    def clientConnectionFailed(self, connector, reason):
        reactor.stop()

if __name__ == "__main__":
    reactor.connectTCP('irc.freenode.net', 6667, TranslateBotFactory())
    reactor.run()
