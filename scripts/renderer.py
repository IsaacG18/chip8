import pygame
import numpy as np


class Renderer:
    def __init__(self, scales):
        self.cols = 64
        self.rows = 32
        self.scales = scales
        self.pixels = np.zeros(self.cols*self.rows)
        self.pixels_old = np.zeros(self.cols*self.rows)
        self.screen = pygame.display.set_mode((self.cols*scales, self.rows*scales))
        self.white = np.array([255,255,255])
        self.black = np.array([0,0,0])

    def render(self):
        self.screen.fill(self.black)
        for location in range(np.size(self.pixels)):
            self.draw_pixel(location)
        pygame.display.update()
    def quick_render(self):
        change = self.pixels - self.pixels_old
        zeros = np.argwhere(change == -1) 
        ones = np.argwhere(change == 1) 
        for one in ones:
            self.quick_draw_pixel(one[0], self.white)
        for zero in zeros:
            self.quick_draw_pixel(zero[0], self.black)
        self.pixels_old = self.pixels.copy()
        pygame.display.update()
        
    def quick_draw_pixel(self,location, colour):
        row,col = location//self.cols, location%self.cols
        pygame.draw.rect(self.screen, colour, 
        pygame.Rect(col*self.scales, row*self.scales, self.scales, self.scales))

    def draw_pixel(self,location):
        row,col = location//self.cols, location%self.cols
        pygame.draw.rect(self.screen, (self.white*self.pixels[location]), 
        pygame.Rect(col*self.scales, row*self.scales, self.scales, self.scales))

    def setPixel(self,col,row):
        col_range = False
        row_range = False
        while not col_range:
            if col>self.cols:
                print(col,row)
                col -= self.cols
            elif col<0:
                print(col,row)
                col += self.cols
            else:
                col_range = True
        while not row_range:
            if row>self.rows:
                print(col,row)
                row -= self.rows
            elif row<0:
                print(col,row)
                row += self.rows
            else:
                row_range = True
        pixelLoc = col + ((row-1)*self.cols)
        self.pixels[pixelLoc] = int(self.pixels[pixelLoc])^1
        
        return not self.pixels[pixelLoc]
    def clear(self):
        self.pixels = np.zeros(self.cols*self.rows)
        self.render()
