import pickle
import mbrot
import pygame
import importlib
import colorization_test_provider
pygame.init()

zoom_coords = (-0.8414203500703239, -0.20850157644901862, -0.8414203121078482, -0.2085015384865429)
# zoom_coords = (-0.22584444085605274, -0.7003014963223264, -0.22584363219101547, -0.7003006876572891)
dim = 800
escape = 1000
y_x: list[list[tuple[int, float, float]]] = []
# list[list[tuple[int, float, float]]]
if "y" in input("recalculate (Y/n): ").lower():
    print("Calculating")
    for y_ in range(dim):
        row = []
        y_x.append(row)
        for x_ in range(dim):
            mx, my = mbrot.map_pixel(x_, y_, dim, dim, zoom_coords)
            iters, x_final, y_final = mbrot.point(mx, my, escape)
            row.append((iters, x_final, y_final))
    print("Saving")
    with open("saved_mbrot.pickle", "wb") as f:
        pickle.dump(y_x, f)
    print("Saved")
else:
    print("Loading")
    with open("saved_mbrot.pickle", "rb") as f:
        y_x = pickle.load(f)
    print("Loaded")

screen = pygame.display.set_mode((dim, dim))

while True:
    print("Starting to draw")
    importlib.reload(colorization_test_provider)
    colorization_test_provider.draw(dim, pygame, screen, y_x)
    print("Done drawing")
    """for y in range(dim):
        pygame.display.update()
        for x in range(dim):
            data = y_x[y][x]
            screen.set_at((x, y), colorization_test_provider.color(*data, x, y))
    pygame.display.update()
    print("Done drawing")"""