
import keyboard
import random
import pygame
import time
import neat
import os


global blockMap
global run
formLength = 2
blockMap = []
run = True


winWidth, winHeight = 700, 700
widthMap, heightMap = 10, 10
pgbSizeTiles = 50

clock = pygame.time.Clock()
clock.tick(.5)

pgdImg, appleImg, snakeBody, snakeFace = pygame.image.load(os.path.join("E:\Projects\Machine Learning\Flappy Bird\Snake\img", "BackGround.png")), pygame.image.load(os.path.join("E:\Projects\Machine Learning\Flappy Bird\Snake\img", "Apple.png")), pygame.image.load(
    os.path.join("E:\Projects\Machine Learning\Flappy Bird\Snake\img", "snakeBody.png")), pygame.image.load(os.path.join("E:\Projects\Machine Learning\Flappy Bird\Snake\img", "snakeFace.png"))
pgdImg, appleImg, snakeBody, snakeFace = pygame.transform.scale(pgdImg, (pgbSizeTiles, pgbSizeTiles)), pygame.transform.scale(
    appleImg, (30, 30)), pygame.transform.scale(snakeBody, (pgbSizeTiles, pgbSizeTiles)), pygame.transform.scale(snakeFace, (pgbSizeTiles, pgbSizeTiles))



class Map:


    def __init__(self):
        self.lenSnake = 1


    def draw(self, win):

        for i in range(heightMap):
            for x in range(widthMap):
                win.blit(pgdImg, (i * pgbSizeTiles, x * pgbSizeTiles))



class Snake:


    def __init__(self):
        self.xPos, self.yPos = 0, 0


    def move(self, win, eatApple):  
        run = True

        if keyboard.is_pressed('w') == True and keyboard.is_pressed("d") == False and keyboard.is_pressed("a") == False:
            self.yPos -= pgbSizeTiles
            run = self.colision(newPos=(self.xPos, self.yPos))
            blockMap.append((self.xPos, self.yPos))
            self.draw(win, eatApple)
    
        elif keyboard.is_pressed('s') and keyboard.is_pressed("w") == False and keyboard.is_pressed("d") == False and keyboard.is_pressed("a") == False:
            self.yPos += pgbSizeTiles
            run = self.colision(newPos=(self.xPos, self.yPos))
            blockMap.append((self.xPos, self.yPos))
            self.draw(win, eatApple)

        elif keyboard.is_pressed('d') and keyboard.is_pressed("w") == False and keyboard.is_pressed("s") == False and keyboard.is_pressed("a") == False:
            self.xPos += pgbSizeTiles
            run = self.colision(newPos=(self.xPos, self.yPos))
            blockMap.append((self.xPos, self.yPos))
            self.draw(win, eatApple)
         
        elif keyboard.is_pressed('a') and keyboard.is_pressed("s") == False and keyboard.is_pressed("d") == False and keyboard.is_pressed("w") == False:
            self.xPos -= pgbSizeTiles
            run = self.colision(newPos=(self.xPos, self.yPos))
            blockMap.append((self.xPos, self.yPos))
            self.draw(win, eatApple)
        return run

           
    def colision(self, newPos):
        run = True

        if len(blockMap) != 0:
            firstBlockPos = blockMap[len(blockMap) -1]

            for blockList in blockMap:
                #print(f"if {newPos} is in {blockList}") DEBUG

                if newPos == blockList or firstBlockPos[0] < 0 or firstBlockPos[0] >= 500 or firstBlockPos[1] >= 500 or firstBlockPos[1] < 0:
                    print("FALSE")
                    run = False
        return run

         
# DRAWS THE SNAKE & MAKES SNAKE LONGER WHEN EATEN AN APPLE
    def draw(self, win, eatApple):
      

        if eatApple == False and len(blockMap) > 1:
            win.blit(pgdImg, blockMap[0])
            blockMap.remove(blockMap[0])

        else:
            for cordinates in blockMap:  
                win.blit(snakeFace, cordinates)

        for cordinates in blockMap:
            win.blit(snakeFace, cordinates)

        if len(blockMap) == 0:
            blockMap.remove(blockMap[0])



class Food:

    def __init__(self):
        self.xPos = 0
        self.yPos = 0


    def spawn(self, win):
        APPLESPAWN = True
        while APPLESPAWN:
            self.xPos = random.randint(0, widthMap)
            self.yPos = random.randint(0, heightMap)

            if self.xPos != 10 and self.yPos != 10:  # OR SNAKE IS ON APPLE
                print("---------------------------------------")
                win.blit(appleImg, (self.xPos*pgbSizeTiles + 7, self.yPos*pgbSizeTiles + 7))
                APPLESPAWN = False
                
                
                return [self.xPos * pgbSizeTiles, self.yPos * pgbSizeTiles]




#____________________________ CLASS END ____________________________

def main():
    food, snake, map = Food(), Snake(), Map()
    win, run = pygame.display.set_mode((winWidth, winHeight)), True

    
    map.draw(win)


    applePos = food.spawn(win)

    while run:
        eatApple = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False



# -- CHECKS IF ONE PART OF THE BODY IS ON A APPLE

        for snakeCord in blockMap:
            if tuple(applePos) == snakeCord:
                eatApple = True
                applePos = food.spawn(win)

        
        run = snake.move(win, eatApple)
        #print(run)

        pygame.display.update()
        time.sleep(.4)


main()





    

