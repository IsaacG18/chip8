from sys import displayhook
import pygame
import renderer
import keyboard
import cpu
from datetime import datetime






class Chip8:
    def __init__(self, scales, fps):
        pygame.init()
        pygame.display.set_caption("chip8 emulator")
        self.screen = renderer.Renderer(scales)
        self.fps = fps
        self.fpsInterval = 10 / self.fps
        self.then = datetime.now()
        self.startTime = self.then
        self.keyboard = keyboard.Keyboard()
        self.cpu = cpu.CPU(self.keyboard, self.screen)
        self.cpu.loadSpritesIntoMemory()
        self.cpu.loadRom('/Users/isaacgilbert/OneDrive - University of Glasgow/Documents/Summer stuff/Chip 8 emulator/scripts/roms/Tic-Tac-Toe.ch8')
        self.step()

    def step(self):
        self.screen.render()
        running = True
        while running:
            now = datetime.now()
            elapsed = (now - self.then).total_seconds()
            if (float(elapsed) > self.fpsInterval):
                self.then = now
                running = self.cpu.cycle()
with open("output1.txt","w")as f:
    f.write("first")
program = Chip8(10,60)
