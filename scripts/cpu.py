
from re import T
import numpy as np
import timers
import stack
import random
import pygame
from pygame.locals import *

MEMORY = 4096
PROGRAM_START = 0x200
REG_COUNT = 16
SPEED = 12
class CPU:
    def __init__(self,keyboard,renderer):
        pygame.init()
        self.keyboard = keyboard
        self.memory = bytearray(MEMORY)
        self.stack = stack.Stack()
        self.pause = False
        self.speed = SPEED
        self.renderer = renderer
        self.opcode = 0
        self.timers = {
            'delay': timers.DelayTimer(),
            'sound': timers.SoundTimer() ,
        }
        self.registers = {
            'v': bytearray(REG_COUNT),
            'index': 0,
            'sp': 0,
            'pc': PROGRAM_START
        }
        self.codes = {
            0x0000: self._0XXX,
            0x1000: self.JP_addr,
            0x2000: self.CALL_addr,
            0x3000: self.SE_Vx_byte,
            0x4000: self.SNE_Vx_byte,
            0x5000: self.SE_Vx_Vy,
            0x6000: self.LD_Vx_byte,
            0x7000: self.ADD_Vx_byte,
            0x8000: self._8XXX,
            0x9000: self.SNE_Vx_VY,
            0xA000: self.LD_I_addr,
            0xB000: self.JP_V0_addr,
            0xC000: self.RND_Vx_byte,
            0xD000: self.DRW_Vx_Vy_nibble,
            0xE000: self._EXXX,
            0xF000: self._FXXX,
        }
    def loadRom(self,romName, offset=PROGRAM_START):
        romdata = open(romName, 'rb').read()
        for index, val in enumerate(romdata):
            self.memory[offset + index] = val


    def loadSpritesIntoMemory(self):
        sprites = np.array(
            (
            0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
            0x20, 0x60, 0x20, 0x20, 0x70, # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
            0x90, 0x90, 0xF0, 0x10, 0x10, # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
            0xF0, 0x10, 0x20, 0x40, 0x40, # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90, # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
            0xF0, 0x80, 0x80, 0x80, 0xF0, # C
            0xE0, 0x90, 0x90, 0x90, 0xE0, # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
            0xF0, 0x80, 0xF0, 0x80, 0x80  # F
            )
        )
        for i in range(np.size(sprites)):
            self.memory[i] = sprites[i]
    def cycle(self):
        for i in range(self.speed):
            if not self.pause:
                self.opcode = self.memory[self.registers["pc"]] <<8|self.memory[self.registers["pc"]+1]
                index = self.registers["pc"]
                ind = self.registers["index"]
                d = self.timers["delay"].readTimer()
                with open("output1.txt","a")as f:
                    for i in self.registers["v"]:
                        f.write(hex(i) + " ")
                    
                    f.write(f"\n {hex(self.opcode)}: {index}: {ind}: {d}\n")
                    
            self.executeInstruction()
            if not self.pause:
                self.updateTimers()
            self.timers["sound"].beep()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    self.keyboard.onKeyDown(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyboard.onKeyUp(event.key)
        self.renderer.quick_render()
        return True

    def updateTimers(self):
        self.timers["delay"].countDown()
        self.timers["sound"].countDown()
    def executeInstruction(self):
        self.registers["pc"] += 2
        # try:
        self.codes[self.opcode & 0xF000]()
        # except: pass
        



    def CLS(self):
        self.renderer.clear() # 00E0
    def RET(self):
        self.registers["pc"] = self.stack.pop() # 00EE
    def JP_addr(self):
        self.registers["pc"] = self.opcode & 0xFFF # 1nnn 
    def CALL_addr(self):
        self.stack.push(self.registers["pc"])
        self.registers["pc"] = self.opcode & 0xFFF # 2nnn
    def SE_Vx_byte(self):
        if self.registers["v"][(self.opcode & 0x0F00) >> 8] == self.opcode & 0xFF:
            self.registers["pc"]+=2 # 3xkk
    def SNE_Vx_byte(self):
        if self.registers["v"][(self.opcode & 0x0F00) >> 8] != self.opcode & 0xFF:
            self.registers["pc"]+=2 # 4xkk
    def SE_Vx_Vy(self):
        if self.registers["v"][(self.opcode & 0x0F00) >> 8] == self.registers["v"][(self.opcode & 0x00F0) >> 4]:
            self.registers["pc"]+=2 # 5xy0
    def LD_Vx_byte(self):
        self.registers["v"][(self.opcode & 0x0F00) >> 8] = self.opcode & 0xFF # 6xkk
    def ADD_Vx_byte(self):
        self.registers["v"][(self.opcode & 0x0F00) >> 8] = (self.registers["v"][(self.opcode & 0x0F00) >> 8] + self.opcode & 0xFF)# 7xkk
    def LD_Vx_Vy(self):
        self.registers["v"][(self.opcode & 0x0F00) >> 8] = self.registers["v"][(self.opcode & 0x00F0) >> 4] # 8xy0
    def OR_Vx_Vy(self):
        self.registers["v"][(self.opcode & 0x0F00) >> 8] = self.registers["v"][(self.opcode & 0x00F0) >> 4] | self.registers["v"][(self.opcode & 0x0F00) >> 8]# 8xy1
    def AND_Vx_Vy(self):
        self.registers["v"][(self.opcode & 0x0F00) >> 8] = self.registers["v"][(self.opcode & 0x00F0) >> 4] & self.registers["v"][(self.opcode & 0x0F00) >> 8]# 8xy2
    def XOR_Vx_Vy(self):
        self.registers["v"][(self.opcode & 0x0F00) >> 8] = self.registers["v"][(self.opcode & 0x00F0) >> 4] ^ self.registers["v"][(self.opcode & 0x0F00) >> 8]# 8xy3
    def ADD_Vx_Vy(self):
        self.registers["v"][0xF] = 0
        value = (self.registers["v"][(self.opcode & 0x0F00) >> 8] + self.registers["v"][(self.opcode & 0x00F0) >> 4]) & 0xFF
        if value > 0xFF:
            self.registers["v"][0XF] = 1 # 8xy4
        self.registers["v"][(self.opcode & 0x0F00) >> 8] = value &0xFF
    def SUB_Vx_Vy(self):
        self.registers["v"][0xF] = 0
        if self.registers["v"][(self.opcode & 0x0F00) >> 8] > self.registers["v"][(self.opcode & 0x00F0) >> 4]:
           self.registers["v"][0xF] = 1 
        self.registers["v"][(self.opcode & 0x0F00) >> 8] = (self.registers["v"][(self.opcode & 0x0F00) >> 8] - self.registers["v"][(self.opcode & 0x00F0) >> 4])&0xFF# 8xy5
    def SHR_Vx(self):
        self.registers["v"][0xF] = (self.registers["v"][(self.opcode & 0x0F00) >> 8] & 0x1)
        self.registers["v"][(self.opcode & 0x0F00) >> 8] >>= 1 # 8xy6
    def SUBN_Vx_Vy(self):
        self.registers["v"][0xF] = 0
        if self.registers["v"][(self.opcode & 0x0F00) >> 8] < self.registers["v"][(self.opcode & 0x00F0) >> 4]:
           self.registers["v"][0xF] = 1 
        self.registers["v"][(self.opcode & 0x0F00) >> 8] = (self.registers["v"][(self.opcode & 0x00F0) >> 4] - self.registers["v"][(self.opcode & 0x0F00) >> 8]) & 0xFF# 8xy7
    def SHL_Vx(self):
        self.registers["v"][0xF] = self.registers["v"][(self.opcode & 0x0F00) >> 8] & 0x800 
        self.registers["v"][(self.opcode & 0x0F00) >> 8] <<=1 # 8xyE
    def SNE_Vx_VY(self):
        if not self.registers["v"][(self.opcode & 0x0F00) >> 8] != self.registers["v"][(self.opcode & 0x00F0) >> 4]:
            self.registers["pc"]+=2 # 9xy0
    def LD_I_addr(self):
        self.registers["index"] = 0xFFF & self.opcode # Annn
    def JP_V0_addr(self):
            self.registers["pc"] = (0xFFF & self.opcode) + self.registers["v"][0] # Bnnn
    def RND_Vx_byte(self):
        self.registers["v"][(self.opcode & 0x0F00) >> 8] = random.randint(0,0xFF)&(0xFF & self.opcode) # Cxkk
    def DRW_Vx_Vy_nibble(self):
        width = 8
        height = self.opcode & 0xF
        self.registers["v"][0xF] = 0
        for row in range(height):
            sprite = self.memory[row + self.registers["index"]]
            for col in range(width):
                if sprite & 0x80 > 0:
                    if self.renderer.setPixel(self.registers["v"][(self.opcode & 0x0F00) >> 8]+col, self.registers["v"][(self.opcode & 0x00F0) >> 4]+row+1):
                        self.registers["v"][0xF] = 1
                sprite <<= 1 # Dxyn
    def SKP_Vx(self):
        if self.keyboard.isKeyPressed(self.registers["v"][(self.opcode & 0x0F00) >> 8]):
            self.registers["pc"] += 2 # Ex9E
    def SKNP_Vx(self):
        if not self.keyboard.isKeyPressed(self.registers["v"][(self.opcode & 0x0F00) >> 8]):
            self.registers["pc"] += 2 # ExA1
    def LD_Vx_DT(self):
        self.registers["v"][(self.opcode & 0x0F00) >> 8] = self.timers["delay"].readTimer() # Fx07
    def  LD_Vx_K(self):
        self.pause = True
        if self.keyboard.anyKeyPressed():
            self.pause = False
            self.registers["v"][(self.opcode & 0x0F00) >> 8] = next(iter(self.keyboard.KeyPressed))
        else:
            self.registers["pc"] -= 2 # Fx0A
    def LD_DT_Vx(self):
        self.timers["delay"].setTimer(self.registers["v"][(self.opcode & 0x0F00) >> 8]) # Fx15
    def LD_ST_Vx(self):
        self.timers["sound"].setTimer(self.registers["v"][(self.opcode & 0x0F00) >> 8]) # Fx18
    def ADD_I_Vx(self):
        self.registers["index"] = self.registers["v"][(self.opcode & 0x0F00) >> 8] + self.registers["index"] # Fx1E
    def LD_F_Vx(self):
        self.registers["index"] = self.registers["v"][(self.opcode & 0x0F00) >> 8] * 5 # Fx29
    def LD_B_Vx(self):
        Vx = (self.opcode & 0x0F00) >> 8
        val = str(self.registers["v"][Vx])
        fillNum = 3 - len(val)
        val = '0' * fillNum + val
        for i in range(len(val)):
            self.memory[self.registers["index"]+i] = int(val[i]) # Fx33
    def LD_I_Vx(self):
        for i in range((self.opcode & 0x0F00) >> 8+1):
            self.memory[self.registers["index"]+ i] = self.registers["v"][i] # Fx55
    def LD_Vx_I(self):
        for i in range(((self.opcode & 0x0F00) >> 8)+1):
            self.registers["v"][i] = self.memory[self.registers["index"]+ i] # Fx65
    def _0XXX(self):
        if self.opcode == 0x00E0:
            self.CLS()
        elif self.opcode == 0x00EE:
            self.RET()
        else:
            return None
    def _8XXX(self):
        if self.opcode & 0xF == 0:
            self.LD_Vx_Vy()
        elif self.opcode & 0xF == 1:
            self.OR_Vx_Vy()
        elif self.opcode & 0xF == 2:
            self.AND_Vx_Vy()
        elif self.opcode & 0xF == 3:
            self.XOR_Vx_Vy()
        elif self.opcode & 0xF == 4:
            self.ADD_Vx_Vy()
        elif self.opcode & 0xF == 5:
            self.SUB_Vx_Vy()
        elif self.opcode & 0xF == 6:
            self.SHR_Vx()
        elif self.opcode & 0xF == 7:
            self.SUBN_Vx_Vy()
        elif self.opcode & 0xE == 0:
            self.SHL_Vx()    
        else:
            return None
    def _EXXX(self):
        if self.opcode & 0xFF == 0x9E:
            self.SKP_Vx()
        elif self.opcode & 0xFF == 0xA1:
            self.SKNP_Vx()
        else:
            return None
    def _FXXX(self):
        if self.opcode & 0xFF == 0x07:
            self.LD_Vx_DT()
        elif self.opcode & 0xFF == 0x0A:
            self.LD_Vx_K()
        elif self.opcode & 0xFF == 0x15:
            self.LD_DT_Vx()
        elif self.opcode & 0xFF == 0x18:
            self.LD_ST_Vx()
        elif self.opcode & 0xFF == 0x1E:
            self.ADD_I_Vx()
        elif self.opcode & 0xFF == 0x29:
            self.LD_F_Vx()
        elif self.opcode & 0xFF == 0x33:
            self.LD_B_Vx()
        elif self.opcode & 0xFF == 0x55:
            self.LD_I_Vx()
        elif self.opcode & 0xFF == 0x65:
            self.LD_Vx_I()
        else:
            return None