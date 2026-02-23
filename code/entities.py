import pygame
from pygame.math import Vector2 as vector
from settings import ANIMATION_SPEED


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, facing_direction):
        super().__init__(groups)

        # graphics
        self.frame_index = 0
        self.frames = frames
        self.facing_direction = facing_direction

        # movement
        self.direction = vector()
        self.speed = 250

        # sprite setup
        self.image = self.frames[self.get_state()][self.frame_index]
        self.rect = self.image.get_frect(center=pos)

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt

        state = self.get_state()
        frames_for_state = self.frames[state]

        self.image = frames_for_state[int(self.frame_index % len(frames_for_state))]

    def get_state(self):
        moving = bool(self.direction)
        if moving:
            if self.direction.x != 0:
                self.facing_direction = 'right' if self.direction.x > 0 else 'left'
            if self.direction.y != 0:
                self.facing_direction = 'down' if self.direction.y > 0 else 'up'

        return f'{self.facing_direction}{"" if moving else "_idle"}'


class Player(Entity):
    def __init__(self, pos, frames, groups, facing_direction):
        super().__init__(pos, frames, groups, facing_direction)

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector()
        if keys[pygame.K_UP]:
            input_vector.y -= 1
        if keys[pygame.K_DOWN]:
            input_vector.y += 1
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
        self.direction = input_vector

    def move(self, dt):
        self.rect.center += self.direction * self.speed * dt

    # calls the update method
    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)


class Character(Entity):
    def __init__(self, pos, frames, groups, facing_direction):
        super().__init__(pos, frames, groups, facing_direction)
