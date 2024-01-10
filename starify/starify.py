import math
import pygame
pygame.init()

RT2 = math.sqrt(2)

inp = pygame.image.load("input.png")

x = inp.get_width()

theta = 360 / 5

theta2 = theta + 45

d = x * RT2

width = round(4 * d * abs(math.cos(math.radians(theta2))) + x)
print(width)

out = pygame.Surface((width, width), pygame.SRCALPHA)

center = round(width / 2) - (5*x/8)

out.fill((0, 255, 0, 255))
# two copies of inp rotated 45 degrees, with the lower corners lined up with the lower corner of the original blit
for i in range(5):
    DIV = 2 * math.asin(math.radians(45/2))
    transform_r = x / DIV
    transform_x = round(transform_r * math.sin(math.radians(i * theta + 180)))
    transform_y = round(transform_r * math.cos(math.radians(i * theta + 180)))
    out.blit(pygame.transform.rotate(inp, i * theta), (center + transform_x, center + transform_y))

lower_right_corner = (width / 2 + x / 2, x)
clockwise_1 = pygame.transform.rotate(inp, 360 - theta)

pygame.image.save(out, "output.png")