import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_RADIUS = 20
BALL_SPEED = 4
SHOOT_DELAY = 500

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

BUBBLE_COLORS = [RED, GREEN, BLUE]

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PUZZLE BUBBLE")

CLOCK = pygame.time.Clock()

class Bubble:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.radius = BALL_RADIUS

    def draw(self):
        pygame.draw.circle(SCREEN, self.color, (self.x, self.y), self.radius)

class Shooter:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - BALL_RADIUS
        self.color = YELLOW
        self.shooting = False
        self.current_bubble = Bubble(random.choice(BUBBLE_COLORS), self.x, self.y)
        self.next_bubble_color = random.choice(BUBBLE_COLORS)

    def shoot(self):
        self.current_bubble = Bubble(self.next_bubble_color, self.x, self.y)
        self.next_bubble_color = random.choice(BUBBLE_COLORS)
        self.shooting = True

    def stop_shooting(self):
        self.shooting = False

    def draw(self):
        self.current_bubble.draw()
        pygame.draw.circle(SCREEN, self.color, (self.x, self.y), BALL_RADIUS)

        # Show the next bubble color at the bottom of the screen
        pygame.draw.circle(SCREEN, self.next_bubble_color, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - BALL_RADIUS * 3), BALL_RADIUS)

bubbles = []
shooter = Shooter()
shoot_timer = 0

def check_collision(bubble1, bubble2):
    distance = ((bubble1.x - bubble2.x) ** 2 + (bubble1.y - bubble2.y) ** 2) ** 0.5
    return distance <= bubble1.radius * 2

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not shooter.shooting and pygame.time.get_ticks() - shoot_timer >= SHOOT_DELAY:
                    shooter.shoot()
                    shoot_timer = pygame.time.get_ticks()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and shooter.x - BALL_SPEED >= BALL_RADIUS:
        shooter.x -= BALL_SPEED
    elif keys[pygame.K_RIGHT] and shooter.x + BALL_SPEED <= SCREEN_WIDTH - BALL_RADIUS:
        shooter.x += BALL_SPEED

    if shooter.shooting:
        shooter.current_bubble.y -= BALL_SPEED
        if shooter.current_bubble.y <= BALL_RADIUS:
            shooter.stop_shooting()
            bubbles.append(shooter.current_bubble)

    SCREEN.fill(BLACK)
    shooter.draw()

    for bubble in bubbles:
        bubble.draw()
        if shooter.shooting and check_collision(shooter.current_bubble, bubble):
            if shooter.current_bubble.color == bubble.color:
                bubbles.remove(bubble)
                shooter.stop_shooting()
                break

    pygame.display.flip()
    CLOCK.tick(60)
