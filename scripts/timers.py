import os

class DelayTimer:
    def __init__(self):
        self.timer = 0
    
    def countDown(self):
        if self.timer > 0:
            self.timer -= 1

    def setTimer(self, value):
        self.timer = value
    
    def readTimer(self):
        return self.timer

class SoundTimer(DelayTimer):
    def __init__(self):
        self.timer = 0
    
    def countDown(self):
        if self.timer > 0:
            self.timer -= 1

    def setTimer(self, value):
        self.timer = value
    
    def readTimer(self):
        return self.timer

    def beep(self):
        if self.timer > 1:
            os.system('play --no-show-progress --null --channels 1 synth %s triangle %f' % (self.timer / 60, 440))
            self.timer = 0