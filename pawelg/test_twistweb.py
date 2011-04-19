from pprint import pformat

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol
from twisted.internet.ssl import ClientContextFactory
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

import zmq

class Context(ClientContextFactory):
    def getContext(self, hostname, port):
        return Client.ContextFactory.getContext(self)

class BeginningPrinter(Protocol):

    def __init__(self, finished):
        context = zmq.Context()
        self.sender = context.socket(zmq.PUSH)
        self.sender.bind('tcp://*:7777')
        self.finished = finished
        self.remaining = 1024 * 10

    def dataReceived(self, bytes):
        if self.remaining:
            display = bytes[:self.remaining]
            print 'Some data received:'
            print display
            self.sender.send(display)
            self.remaining -= len(display)

    def connectionLost(self, reason):
        print 'Finished receiving body:', reason.getErrorMessage()
        self.finished.callback(None)

def cbRequest(response):
    print 'Response version:', response.version
    print 'Response code:', response.code
    print 'Response phrase:', response.phrase
    print 'Response headers:'
    print pformat(list(response.headers.getAllRawHeaders()))
    finished = Deferred()
    response.deliverBody(BeginningPrinter(finished))
    return finished

def cbShutdown(ignored):
    reactor.stop()

def main():
    agent = Agent(reactor)
    d = agent.request('GET', 
                      'http://www.worldtimzone.com/res/vi.html', 
                      Headers({'User-Agent': ['Twisted Web Client Example']}),
                      None)
    d.addCallback(cbRequest)
    d.addBoth(cbShutdown)
    reactor.run()

if __name__ == '__main__':
   main()


