import pygame

class Keyboard:
    def __init__(self):
        self.keymapping = {
            pygame.K_1: 0X1, # 1 to 1 
            pygame.K_2: 0X2, # 2 to 2
            pygame.K_3: 0X3, # 3 to 3
            pygame.K_4: 0Xc, # 4 to c
            pygame.K_q: 0X4, # q to 4
            pygame.K_w: 0X5, # w to 5
            pygame.K_e: 0X6, # e to 6
            pygame.K_r: 0Xd, # r to d
            pygame.K_a: 0X7, # a to 7
            pygame.K_s: 0X8, # s to 8
            pygame.K_d: 0X9, # d to 9
            pygame.K_f: 0Xe, # f to e
            pygame.K_z: 0Xa, # z to a
            pygame.K_x: 0X0, # x to 0
            pygame.K_c: 0Xb, # c to b
            pygame.K_v: 0Xf  # v to f
            } 
        self.KeyPressed = set()

    def isKeyPressed(self, code):
        return code in self.KeyPressed
    
    def anyKeyPressed(self):
        return len(self.KeyPressed) != 0

    def onKeyDown(self,code):
        try:
            self.KeyPressed.add(self.keymapping[code])
        except: pass
        
    def onKeyUp(self,code):
        try:
            self.KeyPressed.remove(self.keymapping[code])
        except: pass