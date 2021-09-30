

import pygame
import math 
import time

from queue import PriorityQueue


width = 800
win = pygame.display.set_mode((width, width))
pygame.display.set_caption("Pathfinding algoritm")


red, green, blue, yellow, white, black, purple, orange, gray, turqoise = (0, 255, 0), (0, 255, 0), (255, 255, 0), (255, 255, 255), (0, 0, 0), (0,191,255), (255, 165, 0), (255, 165, 0), (128, 128, 128), (64, 224, 208)


class Grid__: 

    def __init__(self, row, col, width, totalRows): 
        self.row = row
        self.totalRows = totalRows

        self.col, self.colour = col, white
        self.x, self.y  = row * width, col * width

        self.neighbors = []
        self.width = width

    
    def position(self):
        return self.row, self.col


    def isClosed(self): 
        return self.colour == red


    def isOpen(self):
        return self.colour == green
    

    def isInTheWay(self): 
        return self.colour == black

    
    def isStart(self):
        return self.colour == orange

    
    def isEnd(self): 
        return self.colour == turqoise

    
    def reset(self):
        self.colour = white


    def makeStart(self):
        self.colour = orange


    def makeClosed(self): 
        self.colour = red


    def makeOpen(self): 
        self.colour = green


    def makeBarrier(self): 
        self.colour = black

    
    def makeEnd(self):
        self.colour = turqoise

    
    def makePath(self):
        self.colour = purple

    
    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))        


#-- IF THE NEIGHBORS OF THE SEARTCED BLOCKS ARE NOT A BARRIER & INSIDE THE MAP
#-- THEN APPEND THE CORDINATES OF THE BLOCKS
    def updateNeighbors(self, grid):

	    self.neighbors=[]

	    if self.row < self.totalRows - 1 and not grid[self.row + 1][self.col].isInTheWay(): # DOWN
		    self.neighbors.append(grid[self.row + 1][self.col])

	    if self.row > 0 and not grid[self.row - 1][self.col].isInTheWay(): # UP
		    self.neighbors.append(grid[self.row - 1][self.col])

	    if self.col < self.totalRows - 1 and not grid[self.row][self.col + 1].isInTheWay(): # RIGHT
	    	self.neighbors.append(grid[self.row][self.col + 1]) 

	    if self.col > 0 and not grid[self.row][self.col - 1].isInTheWay(): # LEFT
	    	self.neighbors.append(grid[self.row][self.col - 1])


    def __lt__(self, other):
        return False




# USES MANHATTAN DISTANCE
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.makePath()
		draw()


#-- MAIN ALGO FUNCTION
def aStarAlgo(draw, grid, start, end):
    count = 0 
    openSet = PriorityQueue() # good way to get the lowest value from a que
    openSet.put((0, count, start)) # adds start score to the priority que /count for tie breaker
    cameFrom = {} # keeps track of the previous nodes that was seartched

    gScore = {spot: float("inf") for row in grid for spot in row} # saves the F score of the not seatched nodes / the curent distance from the end node to the start node (colisions not taken to account)
    gScore[start] = 0 # you start at node 0 :)

    fScore = {spot: float("inf") for row in grid for spot in row} # saves the G score of the not seatched nodes /the current smallest distance from the start node to the end node (colisions not taken in to account)
    fScore[start] = h(start.position(), end.position()) # adds a prediction to how far the end node is 

    openSetHash = {start} # adds a hash to modify what is in the priority que

    while not openSet.empty(): # runs untill "openSet" is empty
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # checks if x botton is pressed
                pygame.quit() # quits if the x botton is pressed

        current = openSet.get()[2] # the current node that is beeing looked at
        openSetHash.remove(current) # removes the node that is beeing lookes at from "openSetHash" later from the "PriorityQueue"

        if current == end: # if the seartch is compleate! (found a way from first node to end node) :) :) :)
            reconstruct_path(cameFrom, end, draw)
            end.makeEnd()
            return True 

        for neighbor in current.neighbors: # loops over all of the neighbors of the seartched nodes
            tempGScore = gScore[current] +1 # adds the current gScore to a temp variable 

            if tempGScore < gScore[neighbor]: # if we have found a better gSocre path
                cameFrom[neighbor] = current # adds ot the path that the file has come from
                gScore[neighbor] = tempGScore # updates the gScore
                fScore[neighbor] = tempGScore + h(neighbor.position(), end.position()) # updates the fScore

                if neighbor not in openSetHash: # if the current neighbor has not been found before
                    count += 1 # new block found! :)
                    openSet.put((fScore[neighbor], count, neighbor)) # puts the fScore & count & the neighbor to the "openSet" list
                    openSetHash.add(neighbor) # adds only the spot of the neighbors to the openhash variable
                    neighbor.makeOpen() # open the already searthced spot, so we dont seartch it again

        draw() #draws the result

        if current != start: # if the current node has not been seartced
            current.makeClosed() # maked it closed, so we dont seartch it again

    return False # no path found


def makeGrid(rows, width):
	grid = []
	gap = width // rows
	
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Grid__(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def drawBackground(win, rows, width):
    gap = width // rows

    for i in range(rows):
        pygame.draw.line(win, gray, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, gray, (j * gap, 0), (j * gap, width))


def drawEvrything(win, grid, rows, width):
    win.fill(white)

    for row in grid:
        for spot in row:
            spot.draw(win)


    #drawBackground(win, rows, width)
    pygame.display.update()


def mouseClick(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col







def main(win, width):
    rows = 50
    grid = makeGrid(rows, width)

    start = None
    end = None 

    run = True
    started = False

    while run:
        drawEvrything(win, grid, rows, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]: 
                pos = pygame.mouse.get_pos()
                row, col = mouseClick(pos, rows, width)
                spot = grid[row][col]

                if not start and spot != end:
                    start = spot
                    start.makeStart()
                
                elif not end and spot != start:
                    end = spot
                    end.makeEnd()

                elif spot != end and spot != start:
                    spot.makeBarrier()
            
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = mouseClick(pos, rows, width)
                spot = grid[row][col]
                spot.reset()

                if spot == start:
                    start = end

                elif spot == end:
                    end = None 

#-- IF STARTED
#-- THEN UPDATE TEHE NEIGHBORS AND RUN THE SEARTCH ALGORYTHM
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started: 
                    for row in grid: 
                        for spot in row:
                            spot.updateNeighbors(grid)

                    aStarAlgo(lambda: drawEvrything(win, grid, rows, width), grid, start, end)
                    


    pygame.quit()


main(win, width)











    











