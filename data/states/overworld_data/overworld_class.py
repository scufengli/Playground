import pygame as pg
from ... import prepare as mp
from ... import tools as mt
import sys
from .game_data import levels

class Node(pg.sprite.Sprite):
    def __init__(self,pos, status, icon_speed):
        super().__init__()
        #img1 = pg.image.load('resources/graphics/background_assets/SwordedLevelOW.png').convert_alpha()
        #locked_img =  pg.transform.scale(img1,(100,80))
        #img2 = pg.image.load('resources/graphics/background_assets/NOSwordedLevelOW.png').convert_alpha()
        #unlocked_img = pg.transform.scale(img2,(100,80))
        self.image = pg.Surface((100,80))
        self.rect = self.image.get_rect(center = pos)
        if status == 'available':
            #self.image.blit(unlocked_img, self.rect)
            self.image.fill('red')
        else:
            #self.image.blit(locked_img, self.rect)
            self.image.fill('grey')
        #self.rect = self.image.get_rect(center = pos)

        self.detection_zone = pg.Rect((self.rect.centerx - icon_speed/2),(self.rect.centery - icon_speed/2),icon_speed,icon_speed)

class Icon(pg.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.pos = pos
        self.image = pg.Surface((20,20))
        dot = pg.image.load('resources/graphics/background_assets/target.png').convert_alpha()
        self.dot = pg.transform.scale(dot, (20, 20))
        #self.image.fill('blue')
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        self.rect.center = self.pos
        self.image.blit(self.dot, self.rect)


class Overworld:
    def __init__(self, start_level, max_level):

        # SET UP
        self.display_surface = mp.SCREEN
        bg = mp.BackGroundGFX['overworld_bg'].convert_alpha()
        self.ovw_bg = pg.transform.scale(bg, (mp.screen_width, mp.screen_height))

        self.max_level = max_level
        self.current_level =  start_level

        # MOVEMENT LOGIC
        self.moving = False
        self.move_direction = pg.math.Vector2(0,0)
        self.speed = 8

        # SPRITES
        self.setup_nodes()
        self.setup_icon()

    def setup_nodes(self):
        self.nodes = pg.sprite.Group()

        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available', self.speed)
                self.nodes.add(node_sprite)
            else:
                node_sprite = Node(node_data['node_pos'], 'locked', self.speed)
                self.nodes.add(node_sprite)

    def draw_paths(self):
        points = [node['node_pos'] for index, node in enumerate(levels.values()) if index <= self.max_level]
        pg.draw.lines(self.display_surface,'black',False,points, 6)

    def setup_icon(self):
        self.icon = pg.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        keys = pg.key.get_pressed()
        if not self.moving:
            if keys[pg.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data('next')
                self.current_level += 1
                self.moving = True
                print("right")
            elif keys[pg.K_LEFT] and self.current_level > 0:
                self.move_direction = self.get_movement_data('previous')
                self.current_level -= 1
                self.moving = True
                print("left")

    def get_movement_data(self, target):
        start = pg.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        if target == 'next':
            end = pg.math.Vector2(self.nodes.sprites()[self.current_level+1].rect.center)
        else:
            end = pg.math.Vector2(self.nodes.sprites()[self.current_level-1].rect.center)

        return (end-start).normalize()

    def update_icon_pos(self):
        # self.icon.sprite.rect.center = self.nodes.sprites()[self.current_level].rect.center
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pg.math.Vector2(0,0)
        pass


    def run(self):
        self.display_surface.blit(self.ovw_bg, (0,0))
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
