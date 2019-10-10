import math
import numpy
import pygame


WIDTH = 1200
HEIGHT = 600

MAPSIZE = 12
BOXSIZE = HEIGHT/MAPSIZE
FOV = 90

threeDBlockSize = 600/FOV

map =   [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

wallPool = {}
tiles = []
intersections = []

#find a tile in the tiles-array with help of a tile possition (x,y)
def findTile(x,y):
    for tile in tiles:
        if tile.getPos() == (x,y):
            return tile

#generate a 2d map of the matrix map, with a minimum amount of borders
def generateMap(screen):
    nextID = 1

    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            try:
                if map[y][x] != 0: #Box exists
                    currentTile = tile(x*BOXSIZE, y*BOXSIZE, screen)
                    tiles.append(currentTile)

                    """HANDELS TILES NORTHEN EDGE """
                    if map[y-1][x] == 0:
                        if map[y][x-1] == 0:    #If the tile to the west doesn't exist
                            wallPool[nextID] = wall(x*BOXSIZE, y*BOXSIZE, x*BOXSIZE+BOXSIZE, y*BOXSIZE, screen) #Create new wall, and append it to the wallpool with a new ID  
                            currentTile.setEdgeID("North", nextID) #tells tile what ID the new wall has in the wallPool
                            nextID += 1 #update ID
                        else:                   #If the tile to the west does exist

                            checkTile = findTile((x-1)*BOXSIZE, y*BOXSIZE) #find the tile to the west in the tile array
                            if checkTile.getEdgeID("North") != None: #If west tile has northern edge
                                ID = checkTile.getEdgeID("North")
                                wallToExtend = wallPool.get(ID)
                                wallToExtend.extendX(x*BOXSIZE+BOXSIZE)
                                currentTile.setEdgeID("North", ID)

                            else:                               #If west tile dont have northern edge
                                wallPool[nextID] = wall(x*BOXSIZE, y*BOXSIZE, x*BOXSIZE+BOXSIZE, y*BOXSIZE, screen) #Create new wall, and append it to the wallpool with a new ID                       
                                currentTile.setEdgeID("North", nextID) #tells tile what ID the new wall has in the wallPool  
                                nextID += 1 #update ID

                    """HANDELS TILES SOUTH EDGE """
                    if map[y+1][x] == 0:    #south
                        if map[y][x-1] == 0:    #if west doesnt exist
                            wallPool[nextID] = wall(x*BOXSIZE, y*BOXSIZE+BOXSIZE, x*BOXSIZE+BOXSIZE, y*BOXSIZE+BOXSIZE, screen)  
                            currentTile.setEdgeID("South", nextID)   
                            nextID += 1 #update ID

                        else:                   #if west does exist             
                            checkTile = findTile((x-1)*BOXSIZE, y*BOXSIZE)
                            if checkTile.getEdgeID("South") != None:
                                ID = checkTile.getEdgeID("South")
                                wallToExtend = wallPool.get(ID)
                                wallToExtend.extendX(x*BOXSIZE+BOXSIZE)
                                currentTile.setEdgeID("South", ID)

                            else:
                                wallPool[nextID] = wall(x*BOXSIZE, y*BOXSIZE+BOXSIZE, x*BOXSIZE+BOXSIZE, y*BOXSIZE+BOXSIZE, screen)   
                                currentTile.setEdgeID("South", nextID)   
                                nextID += 1 #update ID

                    """HANDELS TILES WEST EDGE """
                    if map[y][x-1] == 0:    #west
                        if map[y-1][x] == 0:    #if north doest exist
                            wallPool[nextID] = wall(x*BOXSIZE,y*BOXSIZE, x*BOXSIZE, y*BOXSIZE+BOXSIZE, screen)  
                            currentTile.setEdgeID("West", nextID)   
                            nextID += 1 #update ID

                        else:
                            checkTile = findTile((x)*BOXSIZE, (y-1)*BOXSIZE)
                            if checkTile.getEdgeID("West") != None:
                                ID = checkTile.getEdgeID("West")
                                wallToExtend = wallPool.get(ID)
                                wallToExtend.extendY(y*BOXSIZE+BOXSIZE)
                                currentTile.setEdgeID("West", ID)

                            else:
                                wallPool[nextID] = wall(x*BOXSIZE,y*BOXSIZE, x*BOXSIZE, y*BOXSIZE+BOXSIZE, screen)
                                currentTile.setEdgeID("West", nextID)   
                                nextID += 1 #update ID
                    
                    """HANDELS TILES EAST EDGE """
                    if map[y][x+1] == 0:    #east
                        if map[y-1][x] == 0:
                            wallPool[nextID] = wall(x*BOXSIZE+BOXSIZE, y*BOXSIZE, x*BOXSIZE+BOXSIZE, y*BOXSIZE+BOXSIZE, screen)   
                            currentTile.setEdgeID("East", nextID)   
                            nextID += 1 #update ID
                        else:
                            checkTile = findTile((x)*BOXSIZE, (y-1)*BOXSIZE)
                            if checkTile.getEdgeID("East") != None:
                                ID = checkTile.getEdgeID("East")
                                wallToExtend = wallPool.get(ID)
                                wallToExtend.extendY(y*BOXSIZE+BOXSIZE)
                                currentTile.setEdgeID("East", ID)

                            else: 
                                wallPool[nextID] = wall(x*BOXSIZE+BOXSIZE, y*BOXSIZE, x*BOXSIZE+BOXSIZE, y*BOXSIZE+BOXSIZE, screen) 
                                currentTile.setEdgeID("East", nextID)   
                                nextID += 1 #update ID
            except IndexError:
                pass

#generate a 3d enviroment by taking the distance of each ray
def generate3DEnvironment(screen, posX, posY, particleAngle, rayAngle):  
    for i, point in enumerate(intersections):
        pointX, pointY, angle = point

        dx = posX - pointX
        dy = posY - pointY

        distance = math.pow(math.pow(dx, 2) + math.pow(dy, 2), 0.5)
        
        percentDist = (distance/600)
        blockHeight = 600*(1-percentDist)
        margin = (600 - blockHeight) / 2

        try:
            pygame.draw.rect(screen, (255 -percentDist*255, 255-percentDist*255,255- percentDist*255), [600 + i*threeDBlockSize, margin, threeDBlockSize, blockHeight])
        except TypeError:
            pygame.draw.rect(screen, (0,0,0), [600 + i*threeDBlockSize, margin, threeDBlockSize, blockHeight])

    intersections.clear()

class wall:
    def __init__(self, x1, y1, x2, y2,screen):
        self.screen = screen
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2       
        self.y2 = y2

    def extendX(self, newX):
        self.x2 = newX 

    def extendY(self, newY):
        self.y2 = newY

    def draw(self):
        pygame.draw.line(self.screen, (0, 255, 0), [self.x1, self.y1], [self.x2, self.y2], 2)

    def getStartPoint(self):
        return (self.x1, self.y1)

    def getEndPoint(self):
        return (self.x2, self.y2)

class tile:
    def __init__(self, x, y, screen):
        self.screen = screen

        self.posX = x
        self.posY = y

        self.edgeID = {
            "North": None,
            "South": None,
            "West": None,
            "East": None
        }

    def getPos(self):
        return (self.posX, self.posY)

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), [self.posX, self.posY, BOXSIZE, BOXSIZE])

    def getEdgeID(self, cardinalDirection):
        return self.edgeID.get(cardinalDirection)

    def setEdgeID(self, cardinalDirection, id):
        self.edgeID[cardinalDirection] = id

class ray:
    def __init__(self, x, y, screen, angle):
        self.screen = screen
        self.angle = angle

        self.pos = pygame.Vector2()
        self.pos.x = x
        self.pos.y = x
        
        self.dir = pygame.Vector2()
        self.dir.x = numpy.around(numpy.cos(math.radians(self.angle)), decimals=5) + 0.000001
        self.dir.y = numpy.around(numpy.sin(math.radians(self.angle)), decimals=5) + 0.000001


    #update ray start point
    def update(self, x, y):
        self.pos.x = x
        self.pos.y = y

    #display ray
    def show(self, x, y):
        pygame.draw.line(self.screen, (255, 255, 255), [self.pos.x, self.pos.y], [x, y], 1)

    #check for intersection
    def cast(self, wall):
        self.x1, self.y1 = wall.getStartPoint()
        self.x2, self.y2  = wall.getEndPoint()

        self.x3 = self.pos.x
        self.y3 = self.pos.y
        self.x4 = self.dir.x + self.pos.x
        self.y4 = self.dir.y + self.pos.y
        t = 1
        u = 1

        tt = ((self.x1 - self.x3)*(self.y3 - self.y4)) - ((self.y1 - self.y3)*(self.x3 - self.x4))
        tb = ((self.x1 - self.x2)*(self.y3 - self.y4)) - ((self.y1 - self.y2)*(self.x3 - self.x4))
        if tt != 0 and tb != 0:
            t = tt/tb
        
        ut = ((self.x1 - self.x2)*(self.y1 - self.y3)) - ((self.y1 - self.y2)*(self.x1 - self.x3))
        ub = ((self.x1 - self.x2)*(self.y3 - self.y4)) - ((self.y1 - self.y2)*(self.x3 - self.x4))
        
        if tt != 0 and tb != 0:
            u = -(ut/ub)

        if((t <= 1.0 and t >= 0.0) and u > 0.0):
            return (self.x1 + t * (self.x2 -self.x1), self.y1 + t * (self.y2 - self.y1))
        else:
            return False

    def updateAngle(self, angle):
        self.dir.x = numpy.around(numpy.cos(math.radians(angle)), decimals=5) + 0.000001
        self.dir.y = numpy.around(numpy.sin(math.radians(angle)), decimals=5) + 0.000001

    def getAngle(self):
        return self.angle

class partical:
    def __init__(self, screen):
        self.screen = screen
        self.angle = 90

        #particle default possition
        self.posX = 200
        self.posY = 120
        

        #Holding rays
        self.rays = []

        #Creating rays
        
        for angle in range(0,FOV):
            #if angle%5 == 0:
            r = ray(self.posX, self.posY, self.screen, angle)
            self.rays.append(r)
    
    #check if particle colide with any tile
    def doesColide(self, x ,y):
        for tile in tiles:
            tileX, tileY = tile.getPos()

            if self.posX + x > tileX and self.posX + x < tileX + BOXSIZE and self.posY + y > tileY and self.posY + y < tileY+BOXSIZE:
                return True
                
        return False

    #update particle possition of the particle
    def update(self, x, y):
        if not self.doesColide(x,y):
            self.posX, self.posY = self.posX + x, self.posY + y
        


    def show(self):

        pygame.draw.ellipse(self.screen, (255, 0, 0), [self.posX, self.posY, 5, 5], 2) 

        #check if ray has an intersect
        for i, ray in enumerate(self.rays):
            
            #update ray possition
            ray.update(self.posX, self.posY)

            record = math.inf
            closestX = None
            closestY = None

            
            #check intersect for every wall
            for wallKey in wallPool:
                w = wallPool.get(wallKey)

                #Get intersect point if it exist
                intersectPoint = ray.cast(w)
                if intersectPoint != False:
                    
                    x, y = intersectPoint

                    dist = math.pow(math.pow(x - self.posX, 2) + math.pow(y - self.posY, 2), .5)
                    
                    #check if new intersect is closer than anoter intersect the same ray did on another wall
                    if dist < record:
                        record = dist
                        closestX, closestY = intersectPoint

            #show closest intersect
            if(closestX != None and closestY != None):
                ray.show(closestX, closestY)
                #if there is an intersection with a wall, add the intersectPoint to the intersection array to be displayed in the 3d-enviornment
                intersections.append([round(closestX,1), round(closestY,1), ray.getAngle()])
        
        generate3DEnvironment(self.screen, self.posX, self.posY, self.angle, ray.getAngle())
    
    def rotate(self, dir):
        self.angle += dir

        for i, ray in enumerate(self.rays):
            ray.updateAngle(self.angle-45+i)

def main():
        pygame.init()
        done = False
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()

        generateMap(screen)

        p = partical(screen)

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_LEFT]: p.update(-3 ,0)
            if keys_pressed[pygame.K_RIGHT]: p.update(3, 0)
            if keys_pressed[pygame.K_UP]: p.update(0, -3)
            if keys_pressed[pygame.K_DOWN]: p.update(0, 3)
            if keys_pressed[pygame.K_a]: p.rotate(3)
            if keys_pressed[pygame.K_d]: p.rotate(-3)
            
            p.show()

            for t in tiles:
                t.draw()

            pygame.display.flip()
            screen.fill((0,0,0))
            clock.tick(60) 


if __name__ == "__main__":
    main()
