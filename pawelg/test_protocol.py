from protocol import Blur, Detect, Recognize

import unittest

class TestCommunication(unittest.TestCase):

    def test_detect(self):
        detect_message = Detect()
        detect_message.cascades.append(Detect.FRONT)
        detect_message.cascades.extend([Detect.SIDE, Detect.EYES])
        self.assertEqual(detect_message.cascades, [0, 1, 2])       

    def test_blur(self):
        blur_message = Blur()
        self.assertFalse(blur_message.HasField('intensity'))

        blur_message.intensity = 3
        self.assertEqual(blur_message.intensity, 3)

        blur_message.ClearField('intensity')
        self.assertFalse(blur_message.HasField('intensity'))

        self.assertRaises(TypeError, setattr, blur_message.intensity, 'invalid string type')

        blur_message.regions.add().x = 12345678
        self.assertEqual(blur_message.regions[0].x, 12345678)

        region = Blur.Region()
        #region.x = 10
        #region.y = 11
        #region.width = 12
        #region.height = 13

        blur_message.regions.extend([region])
        print blur_message.ListFields()
        self.assertEqual(blur_message.regions[1].height, 13)

if __name__ == '__main__':
    unittest.main()




