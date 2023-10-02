import pygame, sys, math, os, random, pyautogui

from pygame.sprite import AbstractGroup
pygame.init()

WINDOW_SIZE = (1200, 900)
FPS = 30

screen = pygame.display.set_mode(WINDOW_SIZE)  
pygame.display.set_caption("Knightly Wizard") 
pygame.display.set_icon(pygame.image.load('media/character_sprites/good/default.png'))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
os.system('cls')

font = pygame.font.Font('media/misc/upheaval.ttf', 60)

#character images 
default_img = pygame.image.load('media/character_sprites/good/default.png')
wizard_img = pygame.image.load('media/character_sprites/good/wizard.png')
robes_img = pygame.transform.scale(pygame.image.load('media/character_sprites/good/robes.png'), (100, 92))
wizard_robes_img = pygame.transform.scale(pygame.image.load('media/character_sprites/good/wizard_robes.png'), (100, 92))
armor_img = pygame.transform.scale(pygame.image.load('media/character_sprites/good/armor.png'), (100, 92)).convert_alpha()
armor_helmet_img = pygame.transform.scale(pygame.image.load('media/character_sprites/good/armor_helmet.png'), (100, 92))
zombie_img = pygame.image.load('media/character_sprites/bad/zombie.png')
archer_img = pygame.image.load('media/character_sprites/bad/archer.png')
#skill images
skilltree_img = pygame.image.load('media/misc/skilltree.png')
fasterswingss_img = pygame.image.load('media/skills/fasterswings.png')
wizardhats_img =  pygame.image.load('media/skills/wizardhat.png')
robess_img = pygame.image.load('media/skills/robes.png')
wardss_img = pygame.image.load('media/skills/ward.png')
armors_img = pygame.image.load('media/skills/armor.png')
helmets_img = pygame.image.load('media/skills/helmet.png')
bootss_img = pygame.image.load('media/skills/boots.png')
#misc
cursor_img = pygame.transform.scale(pygame.image.load('media/misc/cursor.png'), (32, 32))
skilltreecursor_img = pygame.transform.scale(pygame.image.load('media/misc/skilltreecursor.png'), (24, 36))
buycursor_img = pygame.transform.scale(pygame.image.load('media/misc/buycursor.png'), (24, 36))
sword_img = pygame.image.load('media/misc/slice.png')
fireball_img = pygame.image.load('media/misc/fireball.png') 
ward_img = pygame.image.load('media/misc/ward.png')
ward_img = pygame.transform.scale(pygame.image.load('media/misc/ward.png'), (160, 160))
healthbar_3_img = pygame.transform.scale(pygame.image.load('media/misc/healthbar_3.png'), (510, 54)) #45% smaller
healthbar_5_img = pygame.transform.scale(pygame.image.load('media/misc/healthbar_5.png'), (797, 54)) #45% smaller
coin_img = pygame.transform.scale(pygame.image.load('media/misc/coin.png'), (56, 56))
skilltree_img = pygame.image.load('media/misc/skilltree.png')
fasterswings_img = pygame.image.load('media/skills/fasterswings.png')
skull_img = pygame.image.load('media/misc/skull.png')

dev_mode = 1

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.img = pygame.image.load('media/character_sprites/good/default.png').convert_alpha()
        self.rect = self.img.get_rect()
        self.rect.center = (self.pos.x, self.pos.y)

        self.img_copy = default_img
        self.speed = 5
        self.range = 80
        self.sword_cooldown = 0
        self.fireball_cooldown = 0
        self.invincibility = 0
        self.max_health = 3
        self.health = 3
        self.money = 60
        self.ward_cooldown = 0
        self.ward_rotate = 0
        self.killcount = 0

        self.faster_swings = False #Done
        self.armor = False #needs to change max hp and hp and setSkin
        self.helmet = False #Needs setSkin
        self.boots = False #Needs setSkin
        self.wizard_hat = False #Needs setSkin
        self.robes = False #Needs setSkin 
        self.ward = False    #Done

    def move(self):
        mouse_pos = pygame.math.Vector2(mx, my)
        angle = math.degrees(math.atan2( (mouse_pos.y - self.pos.y), (mouse_pos.x - self.pos.x))) * (-1)

        if self.boots:
            self.speed = 8

        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            up_angle = math.radians(angle)
            up_vector = pygame.math.Vector2(math.cos(up_angle), -math.sin(up_angle))
            up_vector.normalize()
            up_vector *= self.speed
            self.pos += up_vector
            if dev_mode:
                pygame.draw.line(screen, (255, 0, 0), self.pos, self.pos + (up_vector * 20))
        if key[pygame.K_d]:
            right_angle = angle - 90
            right_angle = math.radians(right_angle)
            right_vector = pygame.math.Vector2(math.cos(right_angle), -math.sin(right_angle))
            right_vector.normalize()
            right_vector *= self.speed
            self.pos += right_vector
            if dev_mode:
                pygame.draw.line(screen, (0, 0, 255), self.pos, self.pos + (right_vector * 20))
        if key[pygame.K_a]:
            left_angle = angle + 90
            left_angle = math.radians(left_angle)
            left_vector = pygame.math.Vector2(math.cos(left_angle), -math.sin(left_angle))
            left_vector.normalize()
            left_vector *= self.speed
            self.pos += left_vector
            if dev_mode:
                pygame.draw.line(screen, (255, 255, 0), self.pos, self.pos + (left_vector * 20))
        if key[pygame.K_s]:
            down_angle = angle - 180
            down_angle = math.radians(down_angle)
            down_vector = pygame.math.Vector2(math.cos(down_angle), -math.sin(down_angle))
            down_vector.normalize()
            down_vector *= self.speed
            self.pos += down_vector
            if dev_mode:
                pygame.draw.line(screen, (255, 0, 255), self.pos, self.pos + (down_vector * 20))

        if key[pygame.K_e] and self.sword_cooldown == 0:
            sword = Sword()
            if self.faster_swings:
                self.sword_cooldown = 45
            else:   
                self.sword_cooldown = 80
        if key[pygame.K_q] and self.wizard_hat and self.fireball_cooldown == 0:
            fireball = Fireball()
            self.fireball_cooldown = 150

    
    def draw(self):
        print(self.img.get_alpha())
        mouse_pos = pygame.math.Vector2(mx, my)
        angle = math.degrees(math.atan2( (mouse_pos.y - self.pos.y), (mouse_pos.x - self.pos.x))) * (-1) - 90
        self.img = pygame.transform.rotate(self.img_copy, angle)
        self.rect = self.img.get_rect(center = self.pos)
        if self.invincibility > 0:
            self.invincibility -= 1
            self.img.set_alpha(self.img.get_alpha() + alpha_factor(self.invincibility))
        screen.blit(self.img, self.rect)
        if dev_mode:
            pygame.draw.rect(screen, (0, 255, 0), self.rect, 1)

        pygame.draw.rect(screen, (255, 24, 40), (106, 43, 142 * self.health, 26))
        pygame.draw.rect(screen, (161, 43, 51), (106, 61, 142 * self.health, 8))
        if self.armor:
            screen.blit(healthbar_5_img, (25, 30, 510, 54))
        else:
            screen.blit(healthbar_3_img, (25, 30, 510, 54))

        screen.blit(coin_img, (30, 100, 140, 140))
        money_text = font.render(str(player.money), False, (255, 255, 255))
        screen.blit(money_text, (110, 98))

        screen.blit(skull_img, (30, 172))
        killcount_text = font.render((str(player.killcount) + "/75"), False, (255, 255, 255))
        screen.blit(killcount_text, (110, 170))

        if self.ward and self.ward_cooldown <= 0:
            ward_rect = (pygame.transform.rotate(ward_img, self.ward_rotate)).get_rect()
            ward_rect.center = player.rect.center
            screen.blit(pygame.transform.rotate(ward_img, self.ward_rotate), ward_rect)
            self.ward_rotate += 1
            pygame.draw.rect(screen, (94, 214, 247), (543, 797, 120, 3))
        elif self.ward:
            pygame.draw.rect(screen, (94, 214, 247), (543, 797, (128/900) * (900 - self.ward_cooldown), 3))
            self.ward_cooldown -= 1


        if self.wizard_hat and self.ward:
            screen.blit(pygame.image.load('media/misc/hotbarQEward.png'), (527,789,1,1))
        elif self.wizard_hat:
            screen.blit(pygame.image.load('media/misc/hotbarQE.png'), (527,800,1,1))
        else:
            screen.blit(pygame.image.load('media/misc/hotbarE.png'), (527,800,1,1))

        if self.sword_cooldown > 0:
            self.sword_cooldown -= 1
            sword_cooldown_solid = pygame.Surface((65, 64))
            sword_cooldown_solid.fill((1,1,1))
            sword_cooldown_solid.set_alpha(self.sword_cooldown * 10)
            screen.blit(sword_cooldown_solid, (607, 808, 75, 78))
        if self.fireball_cooldown > 0:
            self.fireball_cooldown -= 1
            fireball_cooldown_solid = pygame.Surface((65,64))
            fireball_cooldown_solid.fill((1, 1, 1))
            fireball_cooldown_solid.set_alpha(self.fireball_cooldown * 10)
            screen.blit(fireball_cooldown_solid, (535, 808, 75, 78))

    def setSkin(self, x):
        self.img_copy = x

class Sword(pygame.sprite.Sprite):  
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, sword_group)
        self.range = 100
        if player.helmet:
            self.scale = 1
        else:
            self.scale = 0.65

        angle = math.degrees(math.atan2(my - player.pos.y, mx - player.pos.x)) * (-1) - 90
        self.img = pygame.transform.rotozoom(sword_img, angle, self.scale)
        self.rect = self.img.get_rect()
        self.rect.center = (player.pos.x + math.cos(math.radians(angle + 90)) * self.range, player.pos.y - math.sin(math.radians(angle + 90)) * self.range)

        self.creation_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.img, self.rect)
        self.img.set_alpha(self.img.get_alpha() - 50)
        if dev_mode:
                pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)
            
class Fireball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, fireball_group)
        self.pos = pygame.math.Vector2(player.rect.x + player.img.get_width()/2, player.rect.y + player.img.get_height()/2)
        self.angle = math.degrees(math.atan2(my - player.rect.centery, mx - player.rect.centerx)) * (-1) - 90
        self.img = pygame.transform.rotate(pygame.image.load('media/misc/fireball.png'), self.angle)
        self.rect = self.img.get_rect()
        self.rect.center = (self.pos.x, self.pos.y)

        if player.robes:
            self.scale =(self.img.get_width() * 1.5, self.img.get_height() * 1.5)
            self.speed = 15
            self.lifespan = 2500 #2 seconds
        else:
            self.scale = (self.img.get_width(), self.img.get_height())
            self.speed = 10
            self.lifespan = 1750
        self.creation_time = pygame.time.get_ticks()

    def move(self):
        up_vector = pygame.math.Vector2(math.cos(math.radians(self.angle + 90)), -math.sin(math.radians(self.angle + 90)))
        up_vector.normalize()
        up_vector *= self.speed
        self.pos += up_vector

    def draw(self):
        self.rect = self.img.get_rect(center = self.pos)
        screen.blit(pygame.transform.scale(self.img, self.scale), self.rect)
        if dev_mode:
            pygame.draw.rect(screen, (255, 69, 0), self.rect, 1)

class Zombie(pygame.sprite.Sprite):
    def __init__(self, coor):
        pygame.sprite.Sprite.__init__(self, enemy_group)
        self.pos = pygame.math.Vector2(coor[0], coor[1])
        self.img = pygame.image.load('media/character_sprites/bad/zombie.png')
        self.rect = self.img.get_rect()
        self.rect.center = (self.pos.x, self.pos.y)

        self.speed = 3
        self.death = False
        self.i = 1

    def draw(self):
        angle = math.degrees(math.atan2(player.pos.y - self.pos.y, player.pos.x - self.pos.x) * (-1)) - 90
        self.img = pygame.transform.rotate(zombie_img, angle)
        self.rect = self.img.get_rect(center = self.pos)
        if self.death:
            self.img.set_alpha(self.img.get_alpha() - self.i * 150)
            self.i += 1
            if self.img.get_alpha() == 0:
                self.kill()
                player.money += 1
                player.killcount += 1
        screen.blit(self.img, self.rect)
        if dev_mode:
            pygame.draw.rect(screen, (0, 255, 0), self.rect, 1)

    def move(self):
        angle = math.atan2(player.pos.y - self.pos.y, player.pos.x - self.pos.x) * (-1)
        direction_vector = pygame.math.Vector2(math.cos(angle), -math.sin(angle))
        direction_vector.normalize()
        direction_vector *= self.speed
        self.pos += direction_vector
        if dev_mode:
            pygame.draw.line(screen, (255, 0, 0), self.pos, self.pos + (direction_vector * 40))

class Archer(pygame.sprite.Sprite):
    def __init__(self, coor):
        pygame.sprite.Sprite.__init__(self, enemy_group)
        global archer_count
        archer_count += 1
        self.pos = pygame.math.Vector2(coor[0], coor[1])
        self.img = pygame.image.load('media/character_sprites/bad/archer.png')
        self.rect = self.img.get_rect(center = self.pos)

        self.speed = 2
        self.death = False
        self.i = 1
        self.attack = False
        self.attack_cooldown = 0

    def move(self):
        angle = math.atan2(player.pos.y - self.pos.y, player.pos.x - self.pos.x) * (-1)
        if self.attack:
            if self.attack_cooldown <= 0:
                arrow = Arrow(self.pos, angle)
                self.attack_cooldown = 90
        else:
            up_vector = pygame.math.Vector2(math.cos(angle), -math.sin(angle))
            up_vector.normalize()
            up_vector *= self.speed
            self.pos += up_vector
            if self.pos.distance_to(player.pos) <= 500:
                if self.pos.x > 50 and self.pos.x < WINDOW_SIZE[0] - 50 and self.pos.y > 50 and self.pos.y < WINDOW_SIZE[1] - 50:
                    self.attack = True
            if dev_mode:
                pygame.draw.line(screen, (255, 0, 0), self.pos, self.pos + (up_vector * 40))
        self.attack_cooldown -= 1

    def draw(self):
        angle = math.degrees(math.atan2(player.pos.y - self.pos.y, player.pos.x - self.pos.x) * (-1)) - 90
        self.img = pygame.transform.rotate(archer_img, angle)
        self.rect = self.img.get_rect(center = self.pos)
        if self.death:
            self.img.set_alpha(self.img.get_alpha() - self.i * 150)
            self.i += 1
            if self.img.get_alpha() == 0:
                self.kill()
                player.killcount += 1
                player.money += 2
                global archer_count
                archer_count -= 1
                global archer_spawn_cooldown
                archer_spawn_cooldown = 600
        screen.blit(self.img, self.rect)
        if dev_mode:
            pygame.draw.rect(screen, (0, 255, 0), self.rect, 1)

class Arrow(pygame.sprite.Sprite):
    def __init__ (self, pos, angle):
        pygame.sprite.Sprite.__init__(self, enemy_group)
        self.pos = pygame.math.Vector2(pos)
        self.direction = pygame.math.Vector2(math.cos(angle), -math.sin(angle)) * 6
        self.img = pygame.transform.rotate(pygame.image.load('media/misc/arrow.png'), math.degrees(angle) - 90)
        self.rect = self.img.get_rect(center = self.pos)

    def move(self):
        self.pos += self.direction
        self.rect.center =  self.pos
        if self.rect.colliderect(player.rect): #radim ovdje player collision jer sam glup i iskr samo zelim da vise zavrsim ovo
            player.health -= 1
            player.invincibility = 30
            self.kill()

    def draw(self):
        screen.blit(self.img, self.rect)
        if dev_mode:
            pygame.draw.rect(screen, (255, 69, 0), self.rect, 1)

class Healthpack(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, healthpack_group)
        self.pos = pos
        self.img = pygame.image.load('media/misc/healthpack.png')
        self.rect = self.img.get_rect(center = self.pos)
        self.lifespan = 150

    def draw(self):
        screen.blit(self.img, self.rect)
        if self.rect.colliderect(player.rect):
            if player.health < player.max_health:
                player.health += 1
                self.kill()
                global healthpack_count
                healthpack_count -= 1
            else:
                self.kill()
                healthpack_count -= 1
        elif self.lifespan <= 0:
            self.kill()
            healthpack_count -= 1
        self.lifespan -= 1


class Skill(pygame.sprite.Sprite):
    def __init__(self, name, x, y, width, height, price, img, prerequisite_group):
        pygame.sprite.Sprite.__init__(self, skill_group)
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.price = price
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.center = self.x, self.y 
        self.bought = False
        self.prerequisite_group = prerequisite_group
        self.buyable = False
        self.blocked = False
    
    def update(self):
        if len(self.prerequisite_group) == 0:
            self.buyable = True
        else:
            for prerequisite in self.prerequisite_group:
                if type(prerequisite) == list:
                    if prerequisite[0].bought and prerequisite[1].bought:
                        self.buyable = True
                elif prerequisite.bought:
                    self.buyable = True
        if self.blocked:
            self.buyable = False
        
        screen.blit(self.img, self.rect)

        if self.buyable == False:
            solid = pygame.Surface((80, 80))
            solid.fill((0, 0, 0))
            solid.set_alpha(180)
            screen.blit(solid, (self.x - self.width/2, self.y - self.width/2))


        if self.bought: #note to future riki: sljedeci put korisit pygame.draw.lines() i stavi sve u jednu liniju koda
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 7)
        if self.name == "faster_swings" and self.bought:
            player.faster_swings = True
            if wizard_hat.blocked == False:
                pygame.draw.line(screen, (255, 255, 255), (self.rect.centerx - self.width/2, self.rect.centery - 1), (self.rect.centerx - self.width/2 - 58, self.rect.centery - 1), 8)
                pygame.draw.line(screen, (255, 255, 255), (self.rect.centerx - self.width/2 - 55, self.rect.centery), (self.rect.centerx - self.width/2 - 55, self.rect.centery + 70), 8)
            if armor.blocked == False:
                pygame.draw.line(screen, (255, 255, 255), (self.rect.centerx + self.width/2, self.rect.centery - 1), (self.rect.centerx + self.width/2 + 57, self.rect.centery - 1), 8)
                pygame.draw.line(screen, (255, 255, 255), (self.rect.centerx + self.width/2 + 53, self.rect.centery), (self.rect.centerx + self.width/2 + 53, self.rect.centery + 70), 8)
        if self.name == "wizard_hat" and self.bought:
            player.wizard_hat = True
            armor.blocked = True
            player.setSkin(wizard_img)
            pygame.draw.line(screen, (255, 255, 255), (self.rect.centerx - self.width/2, self.rect.centery), (self.rect.centerx - self.width/2 - 21, self.rect.centery), 8)
            pygame.draw.line(screen, (255, 255, 255), (self.rect.centerx - self.width/2 - 18, self.rect.centery), (self.rect.centerx - self.width/2 - 18, self.rect.centery + 87), 8)
            pygame.draw.line(screen, (255, 255, 255), (self.rect.centerx + self.width/2, self.rect.centery), (self.rect.centerx + self.width/2 + 20, self.rect.centery), 8)
            pygame.draw.line(screen, (255, 255, 255), (self.rect.centerx + self.width/2 + 16, self.rect.centery), (self.rect.centerx + self.width/2 + 16, self.rect.centery + 87), 8)
        if self.name == "robes" and self.bought:
            player.robes = True
            player.setSkin(wizard_robes_img)
            pygame.draw.line(screen, (255, 255, 255), (self.rect.centerx - 1, self.rect.centery + self.height/2), (self.rect.centerx - 1, self.rect.centery + self.height/2 + 37), 8)
            pygame.draw.line(screen, (255, 255, 255), (self.rect.centerx - 1, self.rect.centery + self.height/2 + 33), (self.rect.centerx + 52, self.rect.centery + self.height/2 + 33), 8)
        if self.name == "ward" and self.bought:
            player.ward = True
            pygame.draw.line(screen, (255, 255, 255), (self.rect.centerx - 1, self.rect.centery + self.height/2), (self.rect.centerx - 1, self.rect.centery + self.height/2 + 37), 8)
            pygame.draw.line(screen, (255, 255, 255), (self.rect.centerx - 1, self.rect.centery + self.height/2 + 33), (self.rect.centerx - 53, self.rect.centery + self.height/2 + 33), 8)
            if robes.bought:
                pygame.draw.line(screen, (255, 255, 255), (506, 571), (506, 639), 8)
                pygame.draw.line(screen, (255, 255, 255), (506, 635), (560, 635), 8)
        if self.name == "armor" and self.bought:
            player.armor = True
            player.max_health = 5
            player.health = 5
            wizard_hat.blocked = True
            player.setSkin(armor_img)
            pygame.draw.line(screen, (255, 255, 255), (self.rect.centerx - 1, self.rect.centery + self.height/2), (self.rect.centerx - 1, self.rect.centery + self.height/2 + 100), 8)
        if self.name == "helmet" and self.bought:
            player.helmet = True
            player.setSkin(armor_helmet_img)
            pygame.draw.line(screen, (255, 255, 255), (self.rect.centerx, self.rect.centery + self.height/2), (self.rect.centerx, self.rect.centery + self.height/2 + 98), 8)
            pygame.draw.line(screen, (255, 255, 255), (self.rect.centerx, self.rect.centery + self.height/2 + 94), (self.rect.centerx - 53, self.rect.centery + self.height/2 + 94), 8)
        if self.name == "boots" and self.bought:
            player.boots = True

#--------functions--------

def alpha_factor(invincibility):
    mylist = [30, 29, 28, 27, 26, 20, 19, 18, 17, 16, 10, 9, 8, 7, 6]
    for i in mylist:
        if invincibility == i:
            return -150
    return 150

def randomCoords():
    side = random.randint(1, 4)
    if side == 1: #left
        return (-10, random.randint(0, WINDOW_SIZE[1]))
    if side == 2: #top
        return (random.randint(0, WINDOW_SIZE[0]), -10)
    if side == 3: #right
        return (WINDOW_SIZE[0] + 10, random.randint(0, WINDOW_SIZE[1]))
    if side == 4: #bottom
        return (random.randint(0, WINDOW_SIZE[0]), -10)
              
def screenshot():
    screen.fill(((34, 38, 51)))
    player.draw()
    for enemy in enemy_group:
        enemy.draw()
    pygame.draw.rect(screen, (255, 24, 40), (106, 43, 142 * player.health, 26))
    pygame.draw.rect(screen, (161, 43, 51), (106, 61, 142 * player.health, 8))
    if player.armor:
        screen.blit(healthbar_5_img, (25, 30, 510, 54))
    else:
        screen.blit(healthbar_3_img, (25, 30, 510, 54))

    screen.blit(coin_img, (30, 100, 140, 140))
    money_text = font.render(str(player.money), False, (255, 255, 255))
    screen.blit(money_text, (110, 98))
    
    return screen.copy()

def moneyReduce(skill):
    if skill.name == "faster_swings":
        player.money -= 5
    if skill.name == "wizard_hat":
        player.money -= 10
    if skill.name == "robes":
        player.money -= 10
    if skill.name == "ward":
        player.money -= 10
    if skill.name == "armor":
        player.money -= 15
    if skill.name == "helmet":
        player.money -= 15
    if skill.name == "boots":
        player.money -= 20

def restart():
    global player, mx, my, enemy_group, sword_group, fireball_group, archer_spawn_cooldown, archer_count, arrow_group, skill_group, healthpack_count, healthpack_group
    global zombie_spawn_cooldown, zombie_cooldown_factor, archer_spawn_cooldown, archer_cooldown_factor, archer_count, healthpack_count
    global faster_swings, wizard_hat, robes, ward, armor, helmet, boots
    pyautogui.moveTo(960, 300)
    player.pos = pygame.math.Vector2(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2)
    player.max_health = 3
    player.health = 3
    player.money = 0
    player.killcount = 0
    player.setSkin(default_img)
    faster_swings.bought = False
    wizard_hat.bought = False
    robes.bought = False
    ward.bought = False
    boots.bought = False
    armor.bought = False
    helmet.bought = False
    player.faster_swings = False
    player.wizard_hat = False
    player.robes = False
    player.ward = False
    player.boots = False
    player.armor = False
    player.helmet = False
    enemy_group.empty()
    sword_group.remove()
    fireball_group.remove()
    arrow_group.remove()
    zombie_spawn_cooldown = 150
    zombie_cooldown_factor = 0
    archer_spawn_cooldown = 600
    archer_cooldown_factor = 0
    archer_count = 0
    healthpack_count = 0
                

#--------screen functions--------

def victory():
    run = True
    while run:
        screen.fill((34, 38, 51))
        dim = pygame.Surface(WINDOW_SIZE)
        dim.fill((0, 0, 0))
        dim.set_alpha(100)
        screen.blit(dim, (0, 0))
        screen.blit(pygame.image.load('media/misc/victory.png'), (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def defeat(screenshot):
    run = True
    click = False
    while run:
        screen.blit(screenshot, (0, 0))
        dim = pygame.Surface(WINDOW_SIZE)
        dim.fill((0, 0, 0))
        dim.set_alpha(100)
        screen.blit(dim, (0, 0))

        restart_rect = pygame.Rect(492, 570, 225, 60)
        exit_rect = pygame.Rect(528, 630, 165, 50)
        #pygame.draw.rect(screen, (0, 255, 0), exit_rect)

        screen.blit(pygame.image.load('media/misc/defeat.png'), (405, 160))
        #defeat_text = font.render("DEFEAT", False, (255, 255, 255), None)
        #screen.blit(defeat_text, (500, 300))

        mx, my = pygame.mouse.get_pos()
        if restart_rect.collidepoint((mx, my)): 
            restart_text = font.render("Restart", False, (255, 255, 255), None)
            screen.blit(restart_text, (488, 570))
            if click:
                restart()
                run = False
        else:
            restart_text = font.render("Restart", False, (174, 171, 166), None)
            screen.blit(restart_text, (488, 570))
        if exit_rect.collidepoint((mx, my)):
            exit_text = font.render("Exit", False, (255, 255, 255), None)
            screen.blit(exit_text, (540, 630))
            if click:
                pygame.quit()
                sys.exit()
        else:
            exit_text = font.render("Exit", False, (174, 171, 166), None)
            screen.blit(exit_text, (540, 630))
        screen.blit(skilltreecursor_img, (mx, my))

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()

def pause(screenshot):
    click = False
    run = True
    while run:
        screen.blit(screenshot, (0, 0))
        dim = pygame.Surface(WINDOW_SIZE)
        dim.fill((0, 0, 0))
        dim.set_alpha(100)
        screen.blit(dim, (0, 0))

        resume_rect = pygame.Rect(500, 305, 225, 50)
        restart_rect = pygame.Rect(492, 367, 225, 60)
        exit_rect = pygame.Rect(528, 440, 165, 50)
        #pygame.draw.rect(screen, (0, 255, 0), restart_rect)

        mx, my = pygame.mouse.get_pos()
        if resume_rect.collidepoint((mx, my)):
            resume_text = font.render("Resume", False, (255, 255, 255), None)
            screen.blit(resume_text, (500, 295))
            if click:
                restart()
                run = False
        else:
            resume_text = font.render("Resume", False, (174, 171, 166), None)
            screen.blit(resume_text, (500, 295))
        if restart_rect.collidepoint((mx, my)): 
            restart_text = font.render("Restart", False, (255, 255, 255), None)
            screen.blit(restart_text, (488, 366))
            if click:
                restart()
                run = False
        else:
            restart_text = font.render("Restart", False, (174, 171, 166), None)
            screen.blit(restart_text, (488, 366))
        if exit_rect.collidepoint((mx, my)):
            exit_text = font.render("Exit", False, (255, 255, 255), None)
            screen.blit(exit_text, (540, 435))
            if click:
                pygame.quit()
                sys.exit()
        else:
            exit_text = font.render("Exit", False, (174, 171, 166), None)
            screen.blit(exit_text, (540, 435))
        screen.blit(skilltreecursor_img, (mx, my))

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()

def skilltree(screenshot):
    click = False
    if len(skill_group) == 0:
        global faster_swings, wizard_hat, robes, ward, armor, helmet, boots
        faster_swings = Skill("faster_swings", 601, 264, 80, 80, 5, fasterswings_img, [])
        wizard_hat = Skill("wizard_hat", 507, 373, 80, 80, 10, wizardhats_img, [faster_swings])
        robes = Skill("robes", 450, 501, 80, 80, 10, robess_img, [wizard_hat])
        ward = Skill("ward", 564, 501, 80, 80, 10, wardss_img, [wizard_hat])
        armor = Skill("armor", 695, 374, 80, 80, 15, armors_img, [faster_swings])
        helmet = Skill("helmet", 694, 501, 80, 80, 15, helmets_img, [armor])
        boots = Skill("boots", 601, 636, 80, 80, 20, bootss_img, [helmet, [robes, ward]])
    run = True
    while run:
        screen.blit(screenshot, (0, 0))
        screen.blit(skilltree_img, (WINDOW_SIZE[0]/2 - skilltree_img.get_width()/2, WINDOW_SIZE[1]/2 - skilltree_img.get_height()/2))
        
        for skill in skill_group:
            skill.update()

        mx, my = pygame.mouse.get_pos()
        screen.blit(skilltreecursor_img, (mx, my))

        for skill in skill_group:
            if skill.rect.collidepoint((mx, my)) and skill.buyable:
                screen.blit(pygame.image.load(f'media/skillbubbles/{skill.name}_bubble.png'), (mx - 2, my - 2))
                if player.money >= skill.price:
                    if click == True:
                        skill.bought = True
                        moneyReduce(skill)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_x:
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True 
            pygame.display.update()
        pygame.display.update()
        clock.tick(FPS)

def main():
    global player, mx, my, enemy_group, sword_group, fireball_group, archer_spawn_cooldown, archer_count, arrow_group, skill_group, healthpack_count, healthpack_group
    global zombie_spawn_cooldown, zombie_cooldown_factor, archer_spawn_cooldown, archer_cooldown_factor, archer_count, healthpack_count
    enemy_group = pygame.sprite.Group()
    sword_group = pygame.sprite.Group()
    fireball_group = pygame.sprite.Group()
    arrow_group = pygame.sprite.Group()
    healthpack_group = pygame.sprite.Group()
    skill_group = pygame.sprite.Group()
    zombie_spawn_cooldown = 150
    zombie_cooldown_factor = 0
    archer_spawn_cooldown = 600
    archer_cooldown_factor = 0
    archer_count = 0
    healthpack_count = 0
    tutorial_timer = 210
    player = Player(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2 + 200)
    pyautogui.moveTo(960, 300)

    run = True
    while run:
        screen.fill((34, 38, 51))
        mx, my = pygame.mouse.get_pos()
        screen.blit(cursor_img, (mx - cursor_img.get_width()/2, my - cursor_img.get_height()/2, 5, 5))

        if zombie_spawn_cooldown <= 0:
            zombie = Zombie(randomCoords())
            zombie_spawn_cooldown = 150 - zombie_cooldown_factor
            if zombie_cooldown_factor <= 80:
                zombie_cooldown_factor += 2
        zombie_spawn_cooldown -= 1
        if archer_spawn_cooldown <= 0 and archer_count < 2:
            archer = Archer(randomCoords())
            archer_spawn_cooldown = 300 - zombie_cooldown_factor
            if archer_cooldown_factor <= 60:
                archer_cooldown_factor += 2
        archer_spawn_cooldown -= 1

        for healthpack in healthpack_group:
            healthpack.draw()
        for sword in sword_group:
            sword.draw()
            if sword.creation_time + 200 <= pygame.time.get_ticks():
                    sword.kill()
        for fireball in fireball_group:
            fireball.move()
            fireball.draw()
            if fireball.creation_time + fireball.lifespan <= pygame.time.get_ticks():
                fireball.kill()
        for enemy in enemy_group:
            enemy.move()
            enemy.draw()
            if player.rect.colliderect(enemy.rect) and player.invincibility == 0:
                if player.ward and player.ward_cooldown <= 0:
                    player.ward_cooldown = 900 #25 seconds 
                    player.invincibility = 30 #1 second
                else:
                    player.health -= 1
                    player.invincibility = 30
            for sword in sword_group:
                if sword.rect.colliderect(enemy.rect):
                    enemy.death = True
                    if random.randint(1, 10) == 7 and healthpack_count < 1:
                        healthpack = Healthpack(enemy.pos)
                        healthpack_count += 1
            for fireball in fireball_group:
                if fireball.rect.colliderect(enemy.rect):
                    enemy.death = True 
                    fireball.kill()

        if tutorial_timer >= 0:
            tutorial_timer -= 1
            screen.blit(pygame.image.load('media/misc/tutorial.png'), (500, 350))    
        
        if player.health == 0:
            defeat(screenshot())
        if player.killcount == 75:
            victory()

        player.draw() 
        player.move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause(screenshot())
                if event.key == pygame.K_x:
                    skilltree(screenshot())
        pygame.display.update()
        clock.tick(FPS)

main()


