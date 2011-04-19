import os
import sys
import unittest

class TestRamdisk(unittest.TestCase):
 
    def test_ram(self):
        for i in range(10000):
            f_hdd = open('image.jpg', 'rb')
            f_ram = open('/tmp/ramdisk/image_copy.jpg', 'wb')
            f_ram.write(f_hdd.read())
            f_hdd.close()
	    f_hdd.close()

            f_hdd = open('image.jpg', 'rb')
            f_ram = open('/tmp/ramdisk/image_copy.jpg', 'rb')
            self.assertEqual(f_hdd.read(), f_ram.read())
      
class TestHdd(unittest.TestCase):
        
    def _test_hdd(self):
        for i in range(10000):
            f_hdd = open('image.jpg', 'rb')
            f_hd2 = open('/tmp/image_copy.jpg', 'wb')
            f_hd2.write(f_hdd.read())
            f_hdd.close()
            f_hd2.close()

            f_hdd = open('image.jpg', 'rb')
            f_hd2 = open('/tmp/image_copy.jpg', 'rb')
            self.assertEqual(f_hdd.read(), f_hd2.read())
          
if __name__ == '__main__':
    unittest.main()
