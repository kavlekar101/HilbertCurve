import pygame
import colorsys
import math
from PIL import Image
import os
import imageio
import urllib.request

order = 9
N = 2**order
total = N*N
width = 1024
counter = 0
#pic = [pygame.transform.scale(pygame.image.load(os.path.join("Games/Pics","1.jpeg")),(1024,1024))]
url = "https://cdn.images.express.co.uk/img/dynamic/79/285x214/349843_1.jpg"
fhand = urllib.request.urlopen(url)
#im = Image.open("Games/Pics/1.jpeg")
#pix = im.load()
im2 = Image.open(fhand)
pix = im2.load()
show = 3

class Order1:
    def __init__(self):
        self.arr = [[0,0],[0,1],[1,1],[1,0]]

def hilbert(i):
    o = Order1()

    index = i&3
    pos = o.arr[index]
    if(order>1):
        for j in range(order):
            len = 2**j
            if j == 0:
                continue
            i = i>>2
            index = i&3
            if(index == 0):
                temp = pos[1]
                pos[1] = pos[0]
                pos[0] = temp
            elif(index == 1):
                pos[1] +=len
            elif(index == 2):
                pos[0] +=len
                pos[1] +=len
            elif(index == 3):
                temp = len-1-pos[0]
                pos[0] = len-1-pos[1]
                pos[1] = temp
                pos[0] +=len

    return pos


def draw(screen):
    len = width/N
    for i in range(total):
        path.append(hilbert(i))
        path[i][0] = path[i][0]*len+len/2
        path[i][1] = path[i][1]*len+len/2

    for i in range(total-1):
        if(show == 1):
            x1,y1 = path[i][0],path[i][1]
            theta = math.atan(float(float(y1)-513.000001)/float(float(x1)-513.000001))*2+math.pi
            color = colorsys.hsv_to_rgb(math.degrees(theta)/360,1,255)
            pygame.draw.line(screen,color,(x1,y1),(path[i+1][0],path[i+1][1]))
        elif(show == 2):
            x1,y1 = path[i][0],path[i][1]
            percent = float(i)/float(total)
            color = colorsys.hsv_to_rgb(percent,1,255)
            pygame.draw.line(screen,color,(x1,y1),(path[i+1][0],path[i+1][1]))
        elif(show == 3):
            x1,y1,x2,y2 = path[i][0],path[i][1],path[i+1][0],path[i+1][1]
            per1,per2 = float(x1)/float(1024),float(y1)/float(1024)
            p1,p2 = int(round(im2.size[0]*per1)),int(round(im2.size[1]*per2))
            try:
                color = pix[p1,p2]
            except IndexError as i:
                pass
            pygame.draw.line(screen,color,(x1,y1),(x2,y2))
    pygame.display.update()

def main():
    global path, counter
    counter = 0
    path = []
    pygame.init()
    screen = pygame.display.set_mode((width,width))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0,0,0))
        draw(screen)
        if(order<=4):
            counter += 1
        elif(order<=7):
            counter+=10
        elif(order<=9):
            counter +=100
        if counter >= total:
            counter = 0
        path = []

    pygame.quit()

main()
