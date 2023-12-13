from user304_rsf8mD0BOQ_1 import Vector
import simplegui

#Visuals
#Background
IMG ="http://personal.rhul.ac.uk/zkac/393/start%20window%20test.png"
IMG_dims = (1920, 1080)
IMG_centre = (960, 540)
CANVAS_DIMS = (1280, 720)

class Background: #Draws a background
    def __init__(self, IMG, IMG_centre, IMG_dims, pos):
        self.img = simplegui.load_image(IMG)
        self.img_centre = IMG_centre
        self.img_dims = IMG_dims
        self.pos = pos
        self.radius = CANVAS_DIMS

    def draw(self, canvas):
        canvas.draw_image(self.img, self.img_centre, self.img_dims, self.pos, self.radius)
        
#Sprites Images
playerSprite_idleRight = simplegui.load_image('http://personal.rhul.ac.uk/zkac/393/test/right%20idle.png')
playerSprite_idleLeft = simplegui.load_image('http://personal.rhul.ac.uk/zkac/393/test/idle%20left.png')
playerSprite_moveRight = simplegui.load_image('http://personal.rhul.ac.uk/zkac/393/test/right%20running.png')
playerSprite_moveLeft = simplegui.load_image('http://personal.rhul.ac.uk/zkac/393/test/left%20running.png')
playerSprite_img = playerSprite_idleRight

coinSpriteSheet_img = simplegui.load_image('http://personal.rhul.ac.uk/zkac/393/test/coin.png')
doorSprite_img = simplegui.load_image('http://personal.rhul.ac.uk/zkac/393/test/Door.png')
keySprite_img = simplegui.load_image('http://personal.rhul.ac.uk/zkac/393/test/key.png')

walkerSprite_moveRight = simplegui.load_image('http://personal.rhul.ac.uk/zkac/393/test/robo%20right.png')
walkerSprite_moveLeft = simplegui.load_image('http://personal.rhul.ac.uk/zkac/393/test/robo%20left.png')

shooterSprite_Left = simplegui.load_image('http://personal.rhul.ac.uk/zkac/393/test/flying%20left.png')
shooterSprite_Right = simplegui.load_image('http://personal.rhul.ac.uk/zkac/393/test/flying%20right.png')

projectileSprite_Left = simplegui.load_image('http://personal.rhul.ac.uk/zkac/393/test/proj%20left.png')
projectileSprite_Right = simplegui.load_image('http://personal.rhul.ac.uk/zkac/393/test/proj%20right.png')

coinSprite_img = simplegui.load_image('http://personal.rhul.ac.uk/zkac/393/test/coinsingle.png')
heartSprite_img = simplegui.load_image('http://personal.rhul.ac.uk/zkac/393/test/heart.png')

#Sounds
coinSound = simplegui.load_sound('http://personal.rhul.ac.uk/zkac/173/coinSound.wav')
coinSound.set_volume(0.2)
doorSound = simplegui.load_sound('http://personal.rhul.ac.uk/zkac/173/doorSound.wav')
doorSound.set_volume(0.3)
jumpSound = simplegui.load_sound('http://personal.rhul.ac.uk/zkac/173/jumpSound.wav')
jumpSound.set_volume(0.1)
hitSound = simplegui.load_sound('http://personal.rhul.ac.uk/zkac/173/hitSound.wav')
hitSound.set_volume(0.1)
winSound = simplegui.load_sound('http://personal.rhul.ac.uk/zkac/173/winSound.wav')
winSound.set_volume(0.3)
keySound = simplegui.load_sound('http://personal.rhul.ac.uk/zkac/173/keySound.wav')
keySound.set_volume(0.3)

#Clock
class Clock:
    def __init__(self):
        self.time = 0

    def tick(self):
        self.time += 1

    def transition (self, frame_duration):
        if self.time % frame_duration == 0:
            return True
        
#Keyboard/Mouse
class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.space = False
        self.e = False #Handles interactions
        self.pause = False # Handles pausing
        self.r = False #Handles restarting
        self.newPress = '' #Decides what direction the player is looking

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['d']:
            self.right = True
            self.newPress = 'right'
        if key == simplegui.KEY_MAP['a']:
            self.left = True
            self.newPress = 'left'
        if key == simplegui.KEY_MAP['space']:
            self.space = True
        if key == simplegui.KEY_MAP['e']:
            self.e = True
        if key == simplegui.KEY_MAP['p']:
            if self.pause:
                self.pause = False
            else:
                self.pause = True
        if key == simplegui.KEY_MAP['r']:
            self.r = True
               
    def keyUp(self, key):
        if key == simplegui.KEY_MAP['d']:
            self.right = False
        if key == simplegui.KEY_MAP['a']:
            self.left = False
        if key == simplegui.KEY_MAP['space']:
            self.space = False
        if key == simplegui.KEY_MAP['e']:
            self.e = False
        if key == simplegui.KEY_MAP['r']:
            self.r = False
            
class Button: #Handles clicks on menu screen
    def __init__(self):
        self.click = None

    def click_handler(self, pos):
        self.click = Vector(pos[0], pos[1])

#Platformer Objects
class Player: 
    def __init__(self, pos):
        self.pos = pos
        self.vel = Vector(0,0)
        self.rad = 25
        self.alive = True
        self.on_platform = False

        self.width = 431
        self.height = 53
        #Animation variables
        self.clock = Clock()
        self.frame_index = [0,0]
        self.frame_clock = 0
        self.cols = 6
        self.rows = 1
        self.duration = 10
        self.frames = 1
        self.frame_height  = self.height / self.rows
        self.frame_width = self.width / self.cols
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2
     
    def left(self):
        return self.pos - Vector(self.width/2, 0)
    def right(self):
        return self.pos + Vector(self.width/2, 0)
    def top(self):
        return self.pos - Vector(0, self.rad)
    def bottom(self):
        return self.pos + Vector(0, self.rad)

    def draw(self, canvas, frame_index=None):
        if frame_index is None:
            frame_index = self.frame_index
        self.update()
        sourceCentre = (self.frame_width * frame_index[0] + self.frame_centre_x,
                         self.frame_height * frame_index[1] + self.frame_centre_y)
        sourceSize = (self.frame_width, self.frame_height)
        destSize = (50, 50)
        canvas.draw_image(playerSprite_img, sourceCentre, sourceSize, self.pos.get_p(), destSize)

    def update(self):
        self.pos.add(self.vel)
        self.clock.tick()
        if self.clock.transition(self.duration):
            self.next_frame()
            
    def next_frame(self):
        self.frame_index[0] = (self.frame_index[0] + 1) % self.cols
        self.frames += 1
        if self.frame_index [0] == 0:
            self.frame_index[1] = (self.frame_index[1] + 1) % self.rows
            self.frames += 1

class Platform: #Handles platforms and their collisions
    def __init__(self, left, right, height):
        self.left = left
        self.right = right
        self.height = height
        self.rad = 5
        self.top = self.height - self.rad
        self.bottom = self.height + self.rad
        self.in_collision = set()

    def draw(self, canvas):
        canvas.draw_line([self.left, self.height], [self.right, self.height], self.rad * 2, 'black')

    def hit(self, player):
        bottom = player.bottom()
        top = player.top()
        return (bottom.y > self.top
                and top.y < self.bottom
                and self.left < bottom.x
                and bottom.x < self.right)

    def interact(self, player):
        if self.hit(player):
            if player not in self.in_collision:
                self.in_collision.add(player)
                if player.vel.y >= 0:
                    player.vel.y = 0
                    player.pos.y = self.top - player.rad
                    return True
                else:
                    player.vel.y = 0
        else:
            self.in_collision.discard(player)
        return False
    
class Shooter: #Floating robot that fires laser projectiles
    def __init__(self, pos, projectileVel, projectileRad, interval):
        self.pos = pos
        self.projectileVel = projectileVel
        self.rad = 15
        self.projectileRad = projectileRad
        self.projectileList = []
        self.interval = interval
        #self.spawn is the position at which the projectiles will be created
        if self.projectileVel.x < 0: #moving left
            self.spawn = self.pos.copy().subtract(Vector(self.rad,0))
            self.img = shooterSprite_Left
        if self.projectileVel.x > 0: #moving right
            self.spawn = self.pos.copy().add(Vector(self.rad,0))
            self.img = shooterSprite_Right
        self.timer = simplegui.create_timer(self.interval,self.addProjectile)
        self.timer.start()
        
        self.frame_height  = 43
        self.frame_width = 31
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2

    def addProjectile(self):
        projectile = Projectile(self.spawn.copy(),self.projectileVel,self.projectileRad)
        self.projectileList.append(projectile)
        
    def removeProjectile(self):
        inactiveProjectiles = []
        for projectile in self.projectileList:
            if projectile.pos.x < 0 or projectile.pos.x > CANVAS_DIMS[0]:
                inactiveProjectiles.append(projectile)
        for projectile in inactiveProjectiles:
            self.projectileList.remove(projectile)
        
    def draw(self,canvas):
        sourceCentre = (self.frame_centre_x, self.frame_centre_y)
        sourceSize = (self.frame_width, self.frame_height)
        destSize = (31, 43)
        canvas.draw_image(self.img, sourceCentre, sourceSize, self.pos.get_p(), destSize)
        for projectile in self.projectileList:
            projectile.draw(canvas)
            
    def update(self,player):
        for projectile in self.projectileList:
            projectile.update(player)
        self.removeProjectile()
        
class Projectile: #laser projectile produced by Shooter
    def __init__(self, pos, vel, rad):
        self.pos = pos
        self.vel = vel
        self.rad = rad
        
        self.frame_height  = 10
        self.frame_width = 16
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2
        if self.vel.x < 0: #moving left
            self.img = projectileSprite_Left
        if self.vel.x > 0: #moving right
            self.img = projectileSprite_Right

    def draw(self, canvas): 
        sourceCentre = (self.frame_centre_x, self.frame_centre_y)
        sourceSize = (self.frame_width, self.frame_height)
        destSize = (16, 10)
        canvas.draw_image(self.img, sourceCentre, sourceSize, self.pos.get_p(), destSize)
               
    def update(self,player):
        self.pos.add(self.vel)
        if self.hit(player):
            player.alive = False
        
    def hit(self,player):
        distance = player.pos.copy().subtract(self.pos).length()
        return distance < player.rad + self.rad

class Walker: #Robot that patrols between two points
    def __init__(self, pos, vel, rad, left, right):
        self.pos = pos
        self.vel = vel
        self.rad = rad
        self.left = left
        self.right = right
        self.on_platform = False
        if self.vel.x <0:
            self.img = walkerSprite_moveLeft
        if self.vel.x>0:
            self.img = walkerSprite_moveRight

        self.width = 352
        self.height = 82
        self.cols = 7
        self.rows = 1
        self.duration = 30
        self.clock = Clock()
        self.frames = 1
        self.frame_height  = self.height / self.rows
        self.frame_width = self.width / self.cols
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2
        self.frame_index = [0,0]
        self.frame_clock = 0


    def left(self):
        return self.pos - Vector(self.rad, 0)
    def right(self):
        return self.pos + Vector(self.rad, 0)
    def top(self):
        return self.pos - Vector(0, self.rad)
    def bottom(self):
        return self.pos + Vector(0, self.rad)

    def draw(self, canvas, frame_index=None):
        if frame_index is None:
            frame_index = self.frame_index
        sourceCentre = (self.frame_width * frame_index[0] + self.frame_centre_x,
                         self.frame_height * frame_index[1] + self.frame_centre_y)
        sourceSize = (self.frame_width, self.frame_height)
        destSize = (self.rad*2, self.rad*2)
        canvas.draw_image(self.img, sourceCentre, sourceSize, self.pos.get_p(), destSize)

    def update(self,player):
        self.pos.add(self.vel)
        #flips sprite between the patrol points.
        if self.pos.x < self.left:
            self.vel.x = -self.vel.x
            self.img = walkerSprite_moveRight
        if self.pos.x > self.right:
            self.vel.x = -self.vel.x
            self.img = walkerSprite_moveLeft
        if self.hit(player):
            player.alive = False
        self.clock.tick()
        if self.clock.transition(self.duration):
            self.next_frame()
        
    def hit(self,player):
        distance = player.pos.copy().subtract(self.pos).length()
        return distance < player.rad + self.rad
        
    def next_frame(self):
        self.frame_index[0] = (self.frame_index[0] + 1) % self.cols
        self.frames += 1
        if self.frame_index [0] == 0:
            self.frame_index[1] = (self.frame_index[1] + 1) % self.rows
            self.frames += 1
            
class Coin: #Points that can be collected throughout the game
    def __init__(self, pos):
        self.pos = pos
        self.vel = Vector(0,0)
        self.rad = 20
        self.collected = False
        
        self.width = 1193
        self.height = 171
        self.cols = 6
        self.rows = 1
        self.duration = 10
        self.clock = Clock()
        self.frames = 1
        self.frame_height  = self.height / self.rows
        self.frame_width = self.width / self.cols
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2
        self.frame_index = [0,0]
        self.frame_clock = 0

    def draw(self, canvas, frame_index=None):
        if frame_index is None:
            frame_index = self.frame_index
        self.update()
        sourceCentre = (self.frame_width * frame_index[0] + self.frame_centre_x,
                         self.frame_height * frame_index[1] + self.frame_centre_y)
        sourceSize = (self.frame_width, self.frame_height)
        destSize = (40, 40)
        canvas.draw_image(coinSpriteSheet_img, sourceCentre, sourceSize, self.pos.get_p(), destSize)

    def collide(self, player):
        distance = player.pos.copy().subtract(self.pos).length()
        return distance < player.rad + self.rad
    
    def update(self):
        self.clock.tick()
        if self.clock.transition(self.duration):
            self.next_frame()
            
    def next_frame(self):
        self.frame_index[0] = (self.frame_index[0] + 1) % self.cols
        self.frames += 1
        if self.frame_index [0] == 0:
            self.frame_index[1] = (self.frame_index[1] + 1) % self.rows
            self.frames += 1    

class Door: #A collision condition is required to take the player to the next level.
    def __init__(self, pos):
        self.pos = pos
        self.rad = 20
        self.frame_height  = 144
        self.frame_width = 94
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2

    def draw(self, canvas): 
        sourceCentre = (self.frame_centre_x, self.frame_centre_y)
        sourceSize = (self.frame_width, self.frame_height)
        destSize = (40, 70)
        canvas.draw_image(doorSprite_img, sourceCentre, sourceSize, self.pos.get_p(), destSize)

    def collide(self, player):
        distance = player.pos.copy().subtract(self.pos).length()
        return distance < player.rad + self.rad

class Key: #An object that follows the player when collected. Required to take the player to the next level.
    def __init__(self, pos):
        self.pos = pos
        self.rad = 10
        self.hasKey = False #Boolean for if key has been collected

        self.frame_height  = 31
        self.frame_width = 69
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2

    def draw(self, canvas): 
        sourceCentre = (self.frame_centre_x, self.frame_centre_y)
        sourceSize = (self.frame_width, self.frame_height)
        destSize = (30, 20)
        canvas.draw_image(keySprite_img, sourceCentre, sourceSize, self.pos.get_p(), destSize)

    def collide(self, player):
        distance = player.pos.copy().subtract(self.pos).length()
        if distance < player.rad + self.rad:
            self.hasKey = True
            keySound.play()

    def update(self, player):
        self.collide(player)
        if self.hasKey == True:
            if player.vel.x >= 0:
                self.pos = player.pos - Vector(self.rad + player.rad + 5, 0)
            if player.vel.x <= 0:
                self.pos = player.pos + Vector(self.rad + player.rad + 5, 0)
                
#Menu
class Menu:
    def __init__(self, button):
        self.background = Background(IMG, IMG_centre, IMG_dims, (CANVAS_DIMS[0] / 2, CANVAS_DIMS[1] / 2))
        self.button = button

    def draw(self, canvas):
        self.background.draw(canvas)

    def click_pos(self): #returns click position
        clickToReturn = self.button.click
        self.button.click = None
        return clickToReturn

#Game    
class Game: #Handles the game
    def __init__(self, keyboard):
        self.keyboard = keyboard
        self.IMG = 'http://personal.rhul.ac.uk/zkac/393/backrounde.png'
        self.background = Background(self.IMG, IMG_centre, IMG_dims, (CANVAS_DIMS[0] / 2, CANVAS_DIMS[1] / 2) )
        self.level = 1 #current level
        self.attempts = 3 #lives counter
        self.coinCounterCurrent = 0 #counts coins collected at the start of each level
        self.coinTotal = 0 #counts the max coins available over levels passed
        self.gameTimer = 0
        self.win = False
        self.loss = False
        self.getLevel()
       
    def getLevel(self):
        playerSprite_img = playerSprite_idleRight
        playerSprite_width = 425
       
        if self.level == 1:
            self.platforms = [Platform(0,CANVAS_DIMS[0],CANVAS_DIMS[1]), Platform(300,600,600)]
            self.coins = [Coin(Vector(500,570)), Coin(Vector(700,500))]
            self.door = Door(Vector(100,685))
            self.key = Key(Vector(1000,670))
            self.walkers = [Walker(Vector(1100,650),Vector(-0.7,0),25,50,1150)]
            self.shooters = []
            self.player = Player(Vector(400, 600))
        if self.level == 2:
            self.platforms = [Platform(0,CANVAS_DIMS[0],CANVAS_DIMS[1]), Platform(200,400,250), Platform(400,900,550), Platform(900,1100,300), Platform(300,600,400), Platform(1050,1200,620)]
            self.coins = [Coin(Vector(500,640)), Coin(Vector(700,500)), Coin(Vector(900,100)), Coin(Vector(100,200))]
            self.door = Door(Vector(250,215))
            self.key = Key(Vector(100,700))
            self.walkers = [Walker(Vector(600,520),Vector(-0.7,0),25,400,900,)]
            self.shooters = [Shooter(Vector(100,500),Vector(2,0),5,2000)]
            self.player = Player(Vector(1050, 250))
        if self.level == 3:
            self.platforms = [Platform(0,CANVAS_DIMS[0],CANVAS_DIMS[1]), Platform(500,800,600), Platform(100,400,450), Platform(800,1100,450), Platform(500,800,300), Platform(100,400,200)] #(long ,right left , up down)
            self.coins = [Coin(Vector(100,300)), Coin(Vector(1200,300)), Coin(Vector(300, 600)), Coin(Vector(650, 400))]
            self.door = Door(Vector(150,160))
            self.key = Key(Vector(650,670))                                                                           
            self.walkers = [Walker(Vector(1100,650),Vector(0.7,1),10,50,1150), Walker(Vector(1100,650),Vector(-0.7,0),10,50,1150), Walker(Vector(250,400),Vector(-0.7,1),10,100,400), Walker(Vector(250,400),Vector(0.7,0),10,100,400), Walker(Vector(700,250),Vector(0.7,0),30,500,800)]
            self.shooters = [Shooter(Vector(900,400),Vector(2,0),5,1800)] 
            self.player = Player(Vector(650, 600))
        if self.level == 4:
            self.platforms = [Platform(0,CANVAS_DIMS[0],CANVAS_DIMS[1]), Platform(1000,1200,600), Platform(600,800,470), Platform(600,800,300)]
            self.coins = [Coin(Vector(300,680)), Coin(Vector(700,500)), Coin(Vector(500,100))]
            self.door = Door(Vector(700,260))
            self.key = Key(Vector(30,680))
            self.walkers = [Walker(Vector(1150,650),Vector(-0.7,0),25,50,1150), Walker(Vector(50,650),Vector(-0.7,0),25,50,1150)]
            self.shooters = [Shooter(Vector(100,680),Vector(3,0),5,2000), Shooter(Vector(1200,680),Vector(-3,0),5,2000)]
            self.player = Player(Vector(1100, 500))
            
        self.coinCounter = self.coinCounterCurrent #sets coin counter to the number of coins acheived before the current level
        
        if self.attempts == 3 and self.level == 1: #adds start level's max coins to max coin counter
            self.coinTotal += len(self.coins)
            
    def nextLevel(self):
        if self.level < 4:
            self.level += 1
            self.coinCounterCurrent = self.coinCounter
            self.getLevel()
            self.coinTotal += len(self.coins)
        else:
            #Display win screne
            winSound.play()
            self.win = True
                    
    def coinHandler(self): #Handles coin interactions
        inactiveCoins = []
        for c in self.coins:
            if c.collide(self.player):
                coinSound.play()
                inactiveCoins.append(c)
                self.coinCounter += 1
        for c in inactiveCoins:
            self.coins.remove(c)

    def draw(self, canvas): 
        self.update()
        self.background.draw(canvas)
        #coin counter visuals
        canvas.draw_image(coinSprite_img, (183/2,171/2), (183,171), (45,50), (30,30))
        canvas.draw_polygon([(20,20),(20,80),(150,80),(150,20)],5,'black')
        canvas.draw_text(str('X'+str(self.coinCounter).zfill(3)),[70,60],30,'black')
        #life counter visuals
        canvas.draw_image(heartSprite_img, (375/2,325/2), (375,325), (205,50), (30,30))
        canvas.draw_polygon([(180,20),(180,80),(310,80),(310,20)],5,'black')
        canvas.draw_text(str('X'+str(self.attempts).zfill(3)),[230,60],30,'black')
        #time visuals
        canvas.draw_text("Time: " + self.getTime(), [1000, 70], 40, "black")
        
        self.door.draw(canvas)
        self.key.draw(canvas)
        self.player.draw(canvas)
        for c in self.coins:
            c.draw(canvas)
        for p in self.platforms:
            p.draw(canvas)
        for w in self.walkers:
            w.draw(canvas)
        for s in self.shooters:
            s.draw(canvas)

    def update(self):
        global playerSprite_img
        self.key.update(self.player)
        self.coinHandler()
        self.player.update()
        for s in self.shooters:
            s.update(self.player)
        self.gameTimer += 1
        #platform interaction checks
        self.player.on_platform = False
        for p in self.platforms:
            self.player.on_platform |= p.interact(self.player)
            for w in self.walkers:
                w.on_platform |= p.interact(w) 
                if w.on_platform == False:
                    w.vel.add(Vector(0, 0.1))
                w.update(self.player)
                
        if not self.player.on_platform:
            self.player.vel.add(Vector(0, 0.4)) #gravity
        else:
            if self.keyboard.space:
                self.player.vel.add(Vector(0, -9)) #jump
                jumpSound.play()
                
        #left and right movement bound by canvas dimensions
        if self.player.pos.x - self.player.rad > 0:
            if self.keyboard.left:
                self.player.vel.add(Vector(-1, 0))
                playerSprite_img = playerSprite_moveLeft
            elif self.keyboard.newPress == 'left':
                playerSprite_img = playerSprite_idleLeft

        if self.player.pos.x + self.player.rad < CANVAS_DIMS[0]:
            if self.keyboard.right:
                self.player.vel.add(Vector(1, 0))
                playerSprite_img = playerSprite_moveRight
            elif self.keyboard.newPress == 'right':
                playerSprite_img = playerSprite_idleRight

        if self.keyboard.e and self.key.hasKey and self.door.collide(self.player): #goes to next level if conditions met
            self.nextLevel()
            doorSound.play()
        
        if self.player.alive == False:
            self.attempts -= 1 #player loses life if hit
            hitSound.play()
            if self.attempts >= 1: #resets to start of level if lives remaining
                self.getLevel()
            else:
                self.loss = True #displays loss screen

        self.player.vel.x *= 0.75 
   
    def getTime(self): #Handles the visuals of the game timer
        m = str(self.gameTimer // 3600)
        if len(m) < 2:
            m = "0" + m
        s = str(self.gameTimer % 3600 // 60)
        if len(s) < 2:
            s = "0" + s
        p = str(int(round(self.gameTimer % float(60) / 60 * 100)))
        if len(p) < 2:
            p = "0" + p
        return m + ":" + s + "." + p

class Interaction: #Handles what screen is displayed
    def __init__(self, menu, game):
        self.menu = menu
        self.game = game
        self.in_menu = "Menu"
        self.transition_mode = True
        self.keyboard = keyboard
        
    def check(self): # check for click on menu screen (progesses to game screen)
        clicked = self.menu.click_pos()
        if clicked is not None:
            self.in_menu = "Game"

    def draw(self, canvas):   
        self.check()
        if self.in_menu == "Menu":
            self.menu.draw(canvas)
        else:
            if self.game.win == True or self.game.loss == True: #Displays win/loss screen
                canvas.draw_polygon([[0, 0], [CANVAS_DIMS[0], 0], [CANVAS_DIMS[0], CANVAS_DIMS[1]], [0, CANVAS_DIMS[1]]], 1,
                                'blue', 'black')
                if self.game.win == True:
                    canvas.draw_text('Winner!', [(CANVAS_DIMS[0] / 2) - 160,200 ], 100, 'white')
                else:
                    canvas.draw_text('Loser!', [(CANVAS_DIMS[0] / 2) - 140,200 ], 100, 'white')
                canvas.draw_text('Press R to restart', [(CANVAS_DIMS[0] / 2) - 175,600 ], 50, 'white')
                canvas.draw_text('Coins Collected:   '+str(self.game.coinCounter).zfill(3)+' / '+str(self.game.coinTotal).zfill(3), [(CANVAS_DIMS[0] / 2) - 300,350 ], 50, 'white')
                canvas.draw_text('     Time Taken:   '+self.game.getTime(), [(CANVAS_DIMS[0] / 2) - 300,450 ], 50, 'white')
                if self.keyboard.r == True:
                    self.game.win = False
                    self.game.loss = False
                    self.game.gameTimer = 0
                    self.game.level = 1
                    self.game.attempts = 3
                    self.game.coinCounterCurrent = 0
                    self.game.coinTotal = 0
                    self.game.getLevel()
            elif self.keyboard.pause: #Displays pause screen
                canvas.draw_polygon([[0, 0], [CANVAS_DIMS[0], 0],
                                     [CANVAS_DIMS[0], CANVAS_DIMS[1]],
                                     [0, CANVAS_DIMS[1]]], 3,
                                    'blue', 'black')
                
                canvas.draw_text(str('Paused'), [(CANVAS_DIMS[0] / 2) - 150, CANVAS_DIMS[1] / 2], 100, 'white')
                
            else: #Draws game
                self.game.draw(canvas)

keyboard = Keyboard()
button = Button()
timer = Clock()
g=Game(keyboard)
m=Menu(button)
start = Interaction(m, g)

frame = simplegui.create_frame("Test", CANVAS_DIMS[0], CANVAS_DIMS[1])
frame.set_canvas_background('#ff5c5c')
frame.set_keydown_handler(keyboard.keyDown)
frame.set_keyup_handler(keyboard.keyUp)
frame.set_mouseclick_handler(button.click_handler)

frame.set_draw_handler(start.draw)
frame.start()