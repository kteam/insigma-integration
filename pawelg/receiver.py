import zmq

def receiver():
    context = zmq.Context()
    receiver = context.socket(zmq.PULL)
    receiver.connect('tcp://127.0.0.1:7777')
    while True:
        message = receiver.recv()
        print message

if __name__ == '__main__':
    receiver()
