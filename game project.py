import pygame
import random
pygame.init()

window = pygame.display.set_mode((480,384))

entities = ["Player", "NPC"]

### 載入圖檔

GUISprites = [pygame.image.load("assets/backpack.png"), pygame.image.load("assets/health.png")]
TileSprite = pygame.image.load("assets/tile.png")
DoorSprite = pygame.image.load("assets/door.png")
LockSprites = {"red":pygame.image.load("assets/red lock.png"),
               "blue":pygame.image.load("assets/blue lock.png"),
               "yellow":pygame.image.load("assets/yellow lock.png")}
EnemySprites = [pygame.image.load("assets/slime.png"), pygame.image.load("assets/slime2.png")]
KeySprites = [pygame.image.load("assets/red key.png"), pygame.image.load("assets/blue key.png"), pygame.image.load("assets/yellow key.png")]
PlayerSprites = [pygame.image.load("assets/player0.png"), pygame.image.load("assets/player1.png"), pygame.image.load("assets/player2.png"), pygame.image.load("assets/player3.png")]
AttackSprites = [pygame.image.load("assets/attack1.png"), pygame.image.load("assets/attack0.png"), pygame.image.load("assets/attack2.png"), pygame.image.load("assets/attack3.png"),
                 pygame.image.load("assets/attack5.png"), pygame.image.load("assets/attack4.png"), pygame.image.load("assets/attack6.png"), pygame.image.load("assets/attack7.png")]

BackpackSprites= {"red key": KeySprites[0],
                  "blue key": KeySprites[1],
                  "yellow key": KeySprites[2],
                  "sword": pygame.image.load("assets/sword.png"),
                  "gem1": pygame.image.load("assets/gem.png"),
                  "gem2": pygame.image.load("assets/gem.png"),
                  "gem3": pygame.image.load("assets/gem.png"),
                  "gem4": pygame.image.load("assets/gem.png")}

### 設定字形

Font = pygame.font.SysFont("arial", 24, True, False)

text = Font.render("Testing", False, (255,255,255), None)

### 設定變數

backpack = []
timer = 0
alive = True
health = 10

### 設定函式

def collide(a, b):
    return a.x + a.width > b.x and a.x < b.x + b.width and a.y + a.height > b.y and a.y < b.y + b.height
def collect(item):
    global backpack
    if not item in backpack:
        backpack.append(item)

### 設定物件

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.type = "Player"
        self.sprite = PlayerSprites
        self.attackSprites = AttackSprites
        self.frame = 0
        self.invincinbilityFrames = 0
        self.attackFrames = 0
        self.attackRange = 64
        self.cooldown = 0
    def update(self):
        
        if (self.invincinbilityFrames and timer % 2 == 0) or not self.invincinbilityFrames:
            window.blit(self.sprite[self.frame], (self.x, self.y))
        if self.attackFrames:
            #pygame.draw.circle(window, (0, 255, 0), (self.x + 16, self.y + 16), self.attackRange, 5)
            if self.frame == 0:
                window.blit(self.attackSprites[int(0 + (self.attackFrames // 4.5) * 4)], (self.x - 16, self.y + 32))
            elif self.frame == 1:
                window.blit(self.attackSprites[int(1 + (self.attackFrames // 4.5) * 4)], (self.x - 16, self.y - 32))
            elif self.frame == 2:
                window.blit(self.attackSprites[int(2 + (self.attackFrames // 4.5) * 4)], (self.x - 32, self.y - 16))
            elif self.frame == 3:
                window.blit(self.attackSprites[int(3 + (self.attackFrames // 4.5) * 4)], (self.x + 32, self.y - 16))
            

        global health
        for i in room:
            if self.attackFrames:
                if i.type == "NPC" and ((self.x - i.x)**2 + (self.y - i.y)**2)**0.5 <= self.attackRange:
                    if (self.frame == 0 and i.y > self.y) or (self.frame == 1 and i.y < self.y) or (self.frame == 2 and i.x < self.x) or (self.frame == 3 and self.x < i.x):
                        if not i.inv:
                            i.inv = 16
                            i.hp -= 1
                            if i.hp == 0:
                                room.remove(i)
            if i.type == "NPC" and collide(self, i) and self.invincinbilityFrames == 0:
                health -= 1
                self.invincinbilityFrames = 32

        if self.invincinbilityFrames > 0:
            self.invincinbilityFrames -= 1

        if self.attackFrames == 0: 
            if keys[pygame.K_LEFT]:
                self.x -= 2
                self.frame = 2
            if keys[pygame.K_RIGHT]:
                self.x += 2
                self.frame = 3       
            if keys[pygame.K_UP]:
                self.y -= 2
                self.frame = 1
            if keys[pygame.K_DOWN]:
                self.y += 2
                self.frame = 0
            if keys[pygame.K_SPACE] and not self.attacked and self.cooldown == 0 and "sword" in backpack:
                self.attackFrames = 6
                self.cooldown = 16
        else:
            self.attackFrames -= 1
        if self.cooldown > 0:
            self.cooldown -= 1

        self.attacked = keys[pygame.K_SPACE]

        if self.cooldown > 0:       
            pygame.draw.line(window, (0, 255, 0), (448,368), (448 + self.cooldown * 2 ,368), 4)

class NPC():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.type = "NPC"
        self.AI = 2
        self.direction = 0
        self.timer = random.randrange(16,33)
        self.hp = 3
        self.inv = 0
    def update(self):
        if (self.inv and timer % 2 == 0) or not self.inv:
            window.blit(EnemySprites[timer % 16 > 8], (self.x, self.y))
            
        if self.inv:
            self.inv -= 1

        if self.AI == 1:
            if self.direction == 1:
                self.x += 2
            elif self.direction == 2:
                self.x -= 2
            elif self.direction == 3:
                self.y += 2
            elif self.direction == 4:
                self.y -= 2
                
            if self.timer > 0:
                self.timer -= 1
                if self.timer == 0:
                    self.direction = random.randrange(0, 5)
                    if self.direction == 0:
                        self.timer = random.randrange(0, 33)
                    else:
                        self.timer = 16
        elif self.AI == 2:
            self.x += random.randrange(-6, 7)
            self.y += random.randrange(-6, 7)
        elif self.AI == 3:
            if self.hp > 3:
                self.hp = 1
            if self.direction == 1:
                self.x += 1
            elif self.direction == 2:
                self.x -= 1
            elif self.direction == 3:
                self.y += 1
            elif self.direction == 4:
                self.y -= 1

            if self.timer > 0:
                self.timer -= 1
                if self.timer == 0:
                    for player in room:
                        if player.type == "Player":
                            if abs(player.x - self.x) > abs(player.y - self.y):
                                if player.x > self.x:
                                    self.direction = 1
                                elif player.x < self.x:
                                    self.direction = 2
                            else:
                                if player.y > self.y:
                                    self.direction = 3
                                elif player.y < self.y:
                                    self.direction = 4
                    self.timer = 16
class Tile():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.type = "Tile"
        self.sprite = TileSprite
    def update(self):

        for obj in room:
            if obj.type in entities:
                if abs(obj.x - self.x) < abs(obj.y - self.y):
                    if obj.x + obj.width >= self.x and obj.x <= self.x + self.width:
                        if obj.y + obj.height > self.y and obj.y < self.y:
                            obj.y = self.y - obj.height
                        if obj.y < self.y + self.height and obj.y > self.y:
                            obj.y= self.y + self.height
                else:                
                    if obj.y + obj.height >= self.y and obj.y <= self.y + self.height:
                        if obj.x + obj.width > self.x and obj.x < self.x:
                            obj.x = self.x - obj.width
                        if obj.x < self.x + self.width and obj.x > self.x:
                            obj.x= self.x + self.width
                    
        window.blit(self.sprite, (self.x, self.y))

class Door():
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.type = "Door"
        self.sprite = DoorSprite
        self.direction = direction
        self.lock = "none"
    def update(self):

        global last_direction
        global last_pos
        global alive
        
        window.blit(self.sprite, (self.x, self.y))
        if self.lock != "none":
            window.blit(LockSprites[self.lock], (self.x + 16, self.y + 8))
        
        for obj in room:
            if self.lock == "none" or (self.lock + " key" in backpack):
                if obj.type == "Player" and collide(self, obj):
                    last_direction = self.direction
                    if self.direction == "W" or self.direction == "E":
                        last_pos = self.y
                    else:
                        last_pos = self.x
                    alive = False
                    break
            else:
                if abs(obj.x - self.x) < abs(obj.y - self.y):
                    if obj.x + obj.width >= self.x and obj.x <= self.x + self.width:
                        if obj.y + obj.height > self.y and obj.y < self.y:
                            obj.y = self.y - obj.height
                        if obj.y < self.y + self.height and obj.y > self.y:
                            obj.y= self.y + self.height
                else:                
                    if obj.y + obj.height >= self.y and obj.y <= self.y + self.height:
                        if obj.x + obj.width > self.x and obj.x < self.x:
                            obj.x = self.x - obj.width
                        if obj.x < self.x + self.width and obj.x > self.x:
                            obj.x= self.x + self.width

class Item():
    def __init__(self,x , y, item):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.type = "Item"
        self.item = item
        self.sprites = [BackpackSprites[self.item]]
        self.frame = 0
    def update(self):
        #pygame.draw.rect(window, (255, 0 ,0), (self.x + 8, self.y + 8, 16, 16))
        for obj in room:
            if collide(self, obj) and obj.type == "Player":
                collect(self.item)
        if self.item in backpack and self in room:
            room.remove(self)
        else:
            window.blit(self.sprites[self.frame], (self.x, self.y))

### 設定形成關卡的零件

#=======================================#
a =["#######n#######",
    "######   ######",
    "######   ######",
    "#####     #####",
    "#     N       #",
    "w      ?      e",
    "#       N     #",
    "#####     #####",
    "######   ######",
    "######   ######",
    "#######s#######"]
b =["#######n#######",
    "#         #N  #",
    "#N        #   #",
    "###   ####    #",
    "#  #          #",
    "w  #   ?   #  e",
    "#          #  #",
    "#    ####   ###",
    "#   #        N#",
    "#  N#         #",
    "#######s#######"]
c =["#######n#######",
    "##           ##",
    "#             #",
    "#   N     N   #",
    "#             #",
    "w      ?      e",
    "#             #",
    "#   N     N   #",
    "#             #",
    "##           ##",
    "#######s#######"]
alltemp = [a, b, c]
allitem = ["enemy","enemy","enemy","enemy","enemy","enemy",
           "red key","blue key","yellow key",
           "blank","blank"]
class cell():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tc = "none"
        self.bc = "none"
        self.lc = "none"
        self.rc = "none"
        self.temp = alltemp[random.randrange(0, 2)]
        self.ai = random.randrange(1, 4)
        self.item = "none"
    def connect(self):
        for i in maze:
            if i.x == self.x:
                if i.y == self.y - 1 and i.bc == "none":
                    i.bc = "close"
                    self.tc = "close"
                if i.y == self.y + 1 and i.tc == "none":
                    i.tc = "close"
                    self.bc = "close"
            if i.y == self.y:
                if i.x == self.x - 1 and i.rc == "none":
                    i.rc = "close"
                    self.lc = "close"
                if i.x == self.x + 1 and i.lc == "none":
                    i.lc = "close"
                    self.rc = "close"
    def draw(self):
        pygame.draw.rect(window, (50, 50, 50), (232+self.x * 16, 168+self.y * 16, 16, 16), 0)
        pygame.draw.rect(window, (0, 0, 255), (233+self.x * 16, 169+self.y * 16, 14, 14), 2)
        if map_pos[0] == self.x and map_pos[1] == self.y:
            pygame.draw.rect(window, (255, 0, 0), (232+self.x * 16 + 4, 168+self.y * 16 + 4, 8, 8), 0)
    
### 隨機形成關卡

Cell = cell(0, 0)
Cell.item = "sword"
maze = []
maze.append(Cell)

while len(maze) < 16:
    a = random.randrange(0, len(maze))
    b = random.randrange(0, 4)
    c = random.randrange(0, len(allitem))
    
    d = "open"
    if random.randrange(0, 4) == 0 and not "red key" in allitem:
        d = "r"
    if random.randrange(0, 4) == 0 and not "blue key" in allitem:
        d = "b"
    if random.randrange(0, 4) == 0 and not "yellow key" in allitem:
        d = "y"
        
    if b == 0 and maze[a].tc == "none":
        maze[a].tc = d
        Cell = cell(maze[a].x, maze[a].y - 1)
        Cell.bc = d
        if len(allitem) != 0:
            Cell.item = allitem[c]
            allitem.remove(allitem[c])
        maze.append(Cell)
    elif b == 1 and maze[a].bc == "none":
        maze[a].bc = d
        Cell = cell(maze[a].x, maze[a].y + 1)
        Cell.tc = d
        if len(allitem) != 0:
            Cell.item = allitem[c]
            allitem.remove(allitem[c])
        maze.append(Cell)
    elif b == 2 and maze[a].lc == "none":
        maze[a].lc = d
        Cell = cell(maze[a].x - 1, maze[a].y)
        Cell.rc = d
        if len(allitem) != 0:
            Cell.item = allitem[c]
            allitem.remove(allitem[c])
        maze.append(Cell)
    elif b == 3 and maze[a].rc == "none":
        maze[a].rc = d
        Cell = cell(maze[a].x + 1, maze[a].y)
        Cell.lc = d
        if len(allitem) != 0:
            Cell.item = allitem[c]
            allitem.remove(allitem[c])
        maze.append(Cell)
    for i in maze:
        i.connect()
    if len(allitem) == 0:
        allitem = ["gem1","gem2","gem3","gem4"]

### 開始遊戲迴圈

run = True
    
map_pos = [0, 0]

last_direction = ""
last_pos = 224

while run:

    ### 載入房間
    
    room = []

    if last_direction == "N":
        obj = Player(last_pos,288)
        map_pos[1] -= 1
    elif last_direction == "S":
        obj = Player(last_pos,32)
        map_pos[1] += 1
    elif last_direction == "W":
        obj = Player(416,last_pos)
        map_pos[0] -= 1
    elif last_direction == "E":
        obj = Player(32,last_pos)
        map_pos[0] += 1
    else:
        obj = Player(last_pos,287)

    room.append(obj)

    for i in maze:
        if i.x == map_pos[0] and i.y == map_pos[1]:
            currentroom = i

    layout = currentroom.temp

    for i in range(len(layout)):
        for j in range(len(layout[0])):
            if layout[i][j] == "#":
                obj = Tile(32*j,32*i)
            elif layout[i][j] == "N" and currentroom.item == "enemy":
                obj = NPC(32*j,32*i)
                obj.AI = currentroom.ai
                
            elif layout[i][j] == "n":
                if currentroom.tc != "close" and currentroom.tc != "none":
                    obj = Door(32*j,32*i, "N")
                else:
                    obj = Tile(32*j,32*i)
                if currentroom.tc == "r":
                    obj.lock = "red"
                if currentroom.tc == "b":
                    obj.lock = "blue"
                if currentroom.tc == "y":
                    obj.lock = "yellow"
            elif layout[i][j] == "s":
                if currentroom.bc != "close" and currentroom.bc != "none":
                    obj = Door(32*j,32*i, "S")
                else:
                    obj = Tile(32*j,32*i)
                if currentroom.bc == "r":
                    obj.lock = "red"
                if currentroom.bc == "b":
                    obj.lock = "blue"
                if currentroom.bc == "y":
                    obj.lock = "yellow"
            elif layout[i][j] == "e":
                if currentroom.rc != "close" and currentroom.rc != "none":
                    obj = Door(32*j,32*i, "E")
                else:
                    obj = Tile(32*j,32*i)
                if currentroom.rc == "r":
                    obj.lock = "red"
                if currentroom.rc == "b":
                    obj.lock = "blue"
                if currentroom.rc == "y":
                    obj.lock = "yellow"
            elif layout[i][j] == "w":
                if currentroom.lc != "close" and currentroom.lc != "none":
                    obj = Door(32*j,32*i, "W")
                else:
                    obj = Tile(32*j,32*i)
                if currentroom.lc == "r":
                    obj.lock = "red"
                if currentroom.lc == "b":
                    obj.lock = "blue"
                if currentroom.lc == "y":
                    obj.lock = "yellow"

            elif layout[i][j] == "?" and currentroom.item not in backpack:
                if currentroom.item == "red key":
                    obj = Item(32*j, 32*i, "red key")
                elif currentroom.item == "blue key":
                    obj = Item(32*j, 32*i, "blue key")
                elif currentroom.item == "yellow key":
                    obj = Item(32*j, 32*i, "yellow key")
                elif currentroom.item == "sword":
                    obj = Item(32*j, 32*i, "sword")
                elif currentroom.item == "gem1":
                    obj = Item(32*j, 32*i, "gem1")
                elif currentroom.item == "gem2":
                    obj = Item(32*j, 32*i, "gem2")
                elif currentroom.item == "gem3":
                    obj = Item(32*j, 32*i, "gem3")
                elif currentroom.item == "gem4":
                    obj = Item(32*j, 32*i, "gem4")
                
                
            if layout[i][j] != " ":
                room.append(obj)

    ### 主要迴圈

    alive = True

    while run and alive:
        pygame.time.delay(20)

        timer += 1

        window.fill((0,0,0))

        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for obj in room:
            obj.update()

        ### GUI
        # health
        window.blit(GUISprites[1], (0, 352))
        text = Font.render(str(health), False, (255, 255, 255), None)
        window.blit(text,(36, 352))
        # backpack
        window.blit(GUISprites[0], (64, 352))
        for i in range(len(backpack)):
            window.blit(BackpackSprites[backpack[i]], (96 + (i*32), 352))

        if keys[pygame.K_LSHIFT]:
            for i in maze:
                i.draw()

        if health == 0 or ("gem1" in backpack and "gem2" in backpack and "gem3" in backpack and "gem4" in backpack):
            run = False

        pygame.display.update()

### 遊戲視窗關閉

pygame.quit()
