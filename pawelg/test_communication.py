# !!! be aware of possible multiprocessing race conditions
# PUSH&PULL big messages seems problematic 

from protocol import Blur, Detect, Recognize
from  multiprocessing import Process, Queue

import time
import unittest
import zmq

class TestCommunication(unittest.TestCase):
    
    def distributor(self, message):
        context = zmq.Context()
        sender = context.socket(zmq.PUSH)
        sender.bind('tcp://*:7777')
        sender.send(message)
        f = open('image.jpg', 'rb')
        data = zmq.Message(f.read()) 
        data = f.read() 
        sender.send(data)

    def collector(self, queue):
        context = zmq.Context()
        receiver = context.socket(zmq.PULL)
        receiver.connect('tcp://127.0.0.1:7777')
        message = receiver.recv()
        data = receiver.recv()
        queue.put(message)
    
    def create_detect(self):
        self.message_original = Detect()
        self.message_original.cascades.extend([Detect.FRONT, Detect.SIDE, Detect.EYES])
    
    def create_blur(self):        
        self.message_original = Blur()
        
        params = (3, 0.128, 0.512)
        self.message_original.intensity = params[0]
        self.message_original.reconstruction_quality = params[1]
        self.message_original.watermark_strength = params[2]
 
        regions = ((1,2,3,4), (5,6,7,8),(9,10,11,12))
        for r in regions:
            region=Blur.Region()
            region.x, region.y, region.width, region.height = r
            self.message_original.regions.extend([region]) 
        
    def setUp(self):
        #self.create_detect()
        self.create_blur()
        self.string_original = self.message_original.SerializeToString()        

        self.queue = Queue()
        self.clctr = Process(target=self.collector, args=(self.queue,))
        self.dstrb = Process(target=self.distributor, args=(self.string_original,))
        self.dstrb.start()
        self.clctr.start()

    def test_message(self):
        #time.sleep(2)
        string_received = self.queue.get()
        self.assertEqual(string_received, self.string_original)
        message_received = Detect()
        message_received.ParseFromString(string_received)
        #self.assertEqual(message_received, self.message_original)

    def tearDown(self):
        self.dstrb.join()
        self.clctr.join()


if __name__ == '__main__':
    unittest.main()









