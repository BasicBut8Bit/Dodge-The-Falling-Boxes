#Made by Johnathan Preyer 2024
import pygame
from pygame.locals import *
import random
import time

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

tile_size = 100

sky_img = pygame.image.load('imgs/sky.png')

class Player():
    def __init__(self, x, y):
        # Load walking and idle images
        self.idle_image = pygame.transform.scale(pygame.image.load('imgs/walking1.png'), (100, 100))
        self.walking_images = [
            pygame.image.load('imgs/walking2.png'),
            pygame.image.load('imgs/walking3.png')
        ]
        self.walking_images = [pygame.transform.scale(img, (100, 100)) for img in self.walking_images]
        self.image_index = 0
        self.image = self.idle_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animation_timer = pygame.time.get_ticks()

    def update(self):
        dx = 0

        # Movement logic
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx -= 5
        if key[pygame.K_RIGHT]:
            dx += 5

        # Animate walking if moving
        if dx != 0:
            current_time = pygame.time.get_ticks()
            if current_time - self.animation_timer > 200:  # Switch frame every 200 ms
                self.image_index = (self.image_index + 1) % len(self.walking_images)
                self.image = self.walking_images[self.image_index]
                self.animation_timer = current_time
        else:
            # Set idle image when not moving
            self.image = self.idle_image

        # Update player position
        self.rect.x += dx

        # Ensure the player doesn't go off-screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

        # Collision detection with falling boxes
        for box in falling_boxes:
            if self.rect.colliderect(box.rect):
                return False  # Collision detected, end the game

        # Draw the player onto the screen
        screen.blit(self.image, self.rect)
        return True  # Player is still alive


class FallingBox:
    def __init__(self, x, y, speed):
        self.image = pygame.transform.scale(pygame.image.load('imgs/block.png'), (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x * tile_size
        self.rect.y = y
        self.speed = speed

    def update(self):
        # Move the box downward
        self.rect.y += self.speed

        # Remove the box if it goes off-screen
        if self.rect.top > screen_height:
            falling_boxes.remove(self)

        # Draw the box
        screen.blit(self.image, self.rect)

class World:
    def __init__(self, data):
        block_img = pygame.image.load('imgs/block.png')
        self.tile_list = []
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(block_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

# World data
world_data = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Initialize objects
player = Player(500, screen_height - 200)
world = World(world_data)

falling_boxes = []
box_spawn_timer = pygame.time.get_ticks()  # Timer for spawning boxes
game_start_time = time.time()  # Record the start time
spawn_delay = 2000  # Initial delay in milliseconds
box_speed_min = 3  # Minimum falling speed
box_speed_max = 10  # Maximum falling speed


# Game loop
run = True
while run:
    screen.blit(sky_img, (0, 0))

    # Draw world
    world.draw()

    clock.tick(fps)

    # Update player and check if alive
    if not player.update():
        print("Game Over!")  # You can replace this with a game-over screen
        run = False  # Exit the game loop

    # Adjust difficulty
    elapsed_time = time.time() - game_start_time
    spawn_delay = max(500, 2000 - int(elapsed_time * 50))  # Decrease spawn delay over time
    box_speed_min = min(15, 3 + int(elapsed_time / 10))  # Increase minimum speed
    box_speed_max = min(20, 6 + int(elapsed_time / 10))  # Increase maximum speed

    # Spawn falling boxes
    if pygame.time.get_ticks() - box_spawn_timer > spawn_delay:
        box_x = random.randint(1, 8)  # Ensure it aligns with the grid
        falling_boxes.append(FallingBox(box_x, 0, random.randint(box_speed_min, box_speed_max)))
        box_spawn_timer = pygame.time.get_ticks()

    # Update falling boxes
    for box in falling_boxes[:]:
        box.update()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

