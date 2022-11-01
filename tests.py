import unittest
import sys
import program.timers as timers

class TestStringMethods(unittest.TestCase):
    def test_getMinutesToNextEvent(self):
        event = dict(                    
            name="Evening",
            timeInMin = 1230,
            timeStr = "20:30",
            color = "ebb63e",
            brightness = 10,
            lamps = ["65546"])
        minutesToNextEvent = timers.getsMinutesToNextEvent(event)
        print(minutesToNextEvent, " fesfes")

if __name__ == '__main__':
    unittest.main()