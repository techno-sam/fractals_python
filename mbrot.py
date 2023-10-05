# Author: Sam
"""

a + bi

c = x + yi

f(z) = z^2 + c

(a + bi) * (a + bi) = a*a + 2abi - b*b
x_new = (x_old*x_old) - (y_old*y_old)
y_new = 2*x_old*y_old

x_new += x
y_new += y


200

f(f(f(0)))

"""
import math
import random
import time

import pygame
from deque_practice import Deque
import colorization_test_provider
import colorsys
pygame.init()

if __name__ == "__main__":
    screen = pygame.display.set_mode([800*2, 800])
else:
    screen = pygame.Surface((800*2, 800))


zoom = (-2.5, -2, 1.5, 2)  # tuple of min and max coords
# zoom = (-0.7746269311970281, 0.12415248501499525, -0.7746269311875639, 0.1241524850244594)
orig_zoom = zoom
zoom_stack = Deque()

_choices = list(range(800))
random_order = []
while len(_choices) > 0:
    idx = random.randrange(0, len(_choices))
    random_order.append(_choices.pop(idx))


def map_pixel(x: int, y: int, width: int, height: int, zoom_bounds: tuple[float, float, float, float]) -> tuple[float, float]:
    # map x 0 <-> width to -2 <-> +2
    # map y 0 <-> height to -2 <-> +2
    """
    x is a number 0 - width
    we want to remap it so that x=0 corresponds to -2 and x=width corresponds to 2
    """
    x_range = zoom_bounds[2] - zoom_bounds[0]
    y_range = zoom_bounds[3] - zoom_bounds[1]
    return (x/width) * x_range + zoom_bounds[0], (y/height) * y_range + zoom_bounds[1]


def map_pixel_reverse(x: float, y: float, width: int, height: int, zoom_bounds: tuple[float, float, float, float]) -> tuple[int, int]:
    # map x -2 <-> +2 to 0 <-> width
    # map y -2 <-> +2 to 0 <-> height
    """
    x is a number 0 - width
    we want to remap it so that x=0 corresponds to -2 and x=width corresponds to 2
    """
    #         max_x          - min_x
    #         max_y          - min_y
    x_range = zoom_bounds[2] - zoom_bounds[0]
    y_range = zoom_bounds[3] - zoom_bounds[1]
    return round((x-zoom_bounds[0]) / x_range * width), round((y-zoom_bounds[1]) / y_range * height)
#    return (x/width) * x_range + zoom_bounds[0], (y/height) * y_range + zoom_bounds[1]


def absolute(x, y):
    return (x**2+y**2)**0.5


"""def py_point(x, y, escape) -> int:
    #x, y = map_pixel(x, y, 800, 800, zoom)
    curr_x = x
    curr_y = y
    for iters in range(escape):
        old_x = curr_x
        old_y = curr_y
        curr_x = (old_x * old_x) - (old_y * old_y)
        curr_y = 2 * old_x * old_y

        curr_x += x
        curr_y += y
        if absolute(curr_x, curr_y) > 2:
            return iters

    return -1"""


try:
    print("Imported mandelbrot!!!")
    from mandelbrot import point, path, paths  # optimization library written by yours truly
#    raise ImportError
except ImportError:
    print("warning: optimization library not found")
    def point(x, y, escape) -> tuple[int, float, float]:
        #x, y = map_pixel(x, y, 800, 800, zoom)
        curr_x = x
        curr_y = y
        for iters in range(escape):
            old_x = curr_x
            old_y = curr_y
            curr_x = (old_x * old_x) - (old_y * old_y)
            curr_y = 2 * old_x * old_y

            curr_x += x
            curr_y += y
            if absolute(curr_x, curr_y) > 2:
                return iters, curr_x, curr_y

        return -1, curr_x, curr_y

    def path(x, y, escape) -> tuple[tuple[float, float]]:
        #x, y = map_pixel(x, y, 800, 800, zoom)
        curr_x = x
        curr_y = y
        pts: list[tuple[float, float]] = []
        for iters in range(escape):
            old_x = curr_x
            old_y = curr_y
            curr_x = (old_x * old_x) - (old_y * old_y)
            curr_y = 2 * old_x * old_y

            curr_x += x
            curr_y += y
            pts.append((curr_x, curr_y))
            if absolute(curr_x, curr_y) > 2:
                return tuple(pts)

        return tuple()

    def paths(scaled_min_x: float, scaled_min_y: float, scaled_max_x: float, scaled_max_y: float, width: int, height: int, escape: int, resolution: int) -> tuple[int, tuple[tuple[int]]]:
        raise NotImplementedError("please just use the accelerator library")


drag_start = None
prev_zoom = None
kg = True
use_hls = False
path_mode = False
prev_path_mode = path_mode
tracer_points = False
tracer_julia = False
just_juliad = False
just_juliad_end = None


def rainbow(iters, max_iters, dimmer=False) -> tuple[int, int, int]:
    mul = 0.8 if dimmer else 1
    if use_hls:
        return tuple([int(v*255) for v in colorsys.hls_to_rgb(iters/max_iters, 0.5*mul, 1)]) # noqa
    else:
        return tuple([int(v*255) for v in colorsys.hsv_to_rgb(iters/max_iters, 1*mul, 1)]) # noqa


def color(x, y, zoom_coords, escape: int = 1000) -> tuple[int, int, int]:
    # escape = 1000
    x, y = map_pixel(x, y, 800, 800, zoom_coords)
    p, final_x, final_y = point(x, y, escape)
    #print(p)
    try:
        return (0, 0, 0) if p == -1 else rainbow(p, 500)
    except ValueError:
        try:
            return rainbow(p, 10)
        except ValueError:
            return 255, 255, 255


def draw(zoom_coords: tuple[float]|list[float], surf: pygame.Surface, w: int = 800, h: int = 800, escape: int = 1000):
    if path_mode:
        print("Starting path drawing")
        #all_pts_r: list[list[int]] = []
        #all_pts_g: list[list[int]] = []
        """all_pts_b: list[list[int]] = []
        for cx in range(800):
        #    all_pts_r.append([])
        #    all_pts_g.append([])
            all_pts_b.append([])
            for cy in range(800):
        #        all_pts_r[cx].append(0)
        #        all_pts_g[cx].append(0)
                all_pts_b[cx].append(0)
        path_res = 800
        for cx in range(path_res):
            if cx % 10 == 0:
                print(f"{cx/path_res*100:.2f}% done calculating")
            for cy in range(path_res):
                mx, my = map_pixel(cx, cy, path_res, path_res, orig_zoom)
                '''for px, py in path(mx, my, 5):#1000):
                    real_x, real_y = map_pixel_reverse(px, py, 800, 800, zoom)
                    try:
                        all_pts_r[real_x][real_y] += 1
                    except IndexError:
                        pass # went outside, don't care
                for px, py in path(mx, my, 1000):#5000):
                    real_x, real_y = map_pixel_reverse(px, py, 800, 800, zoom)
                    try:
                        all_pts_g[real_x][real_y] += 1
                    except IndexError:
                        pass # went outside, don't care'''
                for px, py in path(mx, my, 100):#500):
                    real_x, real_y = map_pixel_reverse(px, py, 800, 800, zoom)
                    try:
                        all_pts_b[real_x][real_y] += 1
                    except IndexError:
                        pass # went outside, don't care
#        max_val_r = max([max(v) for v in all_pts_r])
#        max_val_g = max([max(v) for v in all_pts_g])
        max_val_b = max([max(v) for v in all_pts_b])"""                         # esc  res
        max_val_r, all_pts_r = paths(zoom[0], zoom[1], zoom[2], zoom[3], 800, 800, 10000, 700)#1600)
        max_val_g, all_pts_g = paths(zoom[0], zoom[1], zoom[2], zoom[3], 800, 800, 100, 1600)
        max_val_b, all_pts_b = paths(zoom[0], zoom[1], zoom[2], zoom[3], 800, 800, 1000, 400)
        #max_val_g = max_val_b = max_val_r
        #all_pts_g = all_pts_b = all_pts_r
        print("Plotting")
        for cx in range(800):
            for cy in range(800):
                r = int((all_pts_r[cx][cy]/max_val_r) * 255)
                g = int((all_pts_g[cx][cy]/max_val_g) * 255)
                b = int((all_pts_b[cx][cy]/max_val_b) * 255)
                screen.set_at((cx, cy), (r, g, b))
            if cx%10 == 0:
                pygame.display.update()
        print("Done")
    else:
        if True:
            for y_idx in range(h):
                cy = random_order[y_idx]
                for cx in range(w):
                    mx_, my_ = map_pixel(cx, cy, w, h, zoom_coords)
                    iters_, fx_, fy_ = point(mx_, my_, escape)
                    surf.set_at((cx, cy), colorization_test_provider.color_counts(iters_, fx_, fy_, cx, cy, {}, 0, escape))
                if y_idx % 10 == 0 and surf == screen:
                    pygame.display.update()
        elif __name__ == "__main__" and False:
            for cx in range(w):
                for cy in range(h):
                    surf.set_at((cx, cy), color(cx, cy, zoom_coords, escape=escape))
                if cx % 10 == 0 and surf == screen:
                    pygame.display.update()
        else:
            avg_escape = 0
            avg_count = 0
            y_x = []
            for cy in range(h):
                row = []
                y_x.append(row)
                for cx in range(w):
                    mx_, my_ = map_pixel(cx, cy, w, h, zoom_coords)
                    it, fx, fy = point(mx_, my_, escape)
                    row.append((it, fx, fy))
                    if it != -1:
                        avg_escape += it
                        avg_count += 1
    #                surf.set_at((cx, cy), color(cx, cy, zoom_coords, escape=escape))
            avg_escape /= avg_count
            if True:
                colorization_test_provider.draw(800, pygame, surf, y_x, display_update=surf==screen, max_iters=escape)
            else:
                for cx in range(w):
                    for cy in range(h):
                        surf.set_at((cx, cy), colorization_test_provider.color(*y_x[cy][cx], cx, cy, avg_escape))
                    if cx%10 == 0 and surf == screen:
                        pygame.display.update()

    if surf == screen:
        pygame.display.update()


def square(min_x, min_y, max_x, max_y):
    """returns new value for max_x, max_y"""
    width, height = max_x - min_x, max_y - min_y
    if width == 0:
        hori_sign = 1
    else:
        hori_sign = width/abs(width)
    if height == 0:
        vert_sign = 1
    else:
        vert_sign = height/abs(height)
    avg = (abs(width) + abs(height)) / 2
    return min_x + avg*hori_sign, min_y + avg*vert_sign


screen_bkp = pygame.Surface((screen.get_width(), screen.get_height()))


if __name__ == "__main__":
    iter_count = 1000
    old_iter_count = iter_count
    while kg:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                kg = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                just_juliad = False
                if drag_start is not None:
                    drag_end = pygame.mouse.get_pos()
                    minx, miny = drag_start
                    maxx, maxy = drag_end
                    maxx, maxy = square(minx, miny, maxx, maxy)

                    minx_bkp = minx
                    miny_bkp = miny

                    minx, miny = min(minx, maxx), min(miny, maxy)
                    maxx, maxy = max(minx_bkp, maxx), max(miny_bkp, maxy)
                    zoom_stack.add_front(zoom)
                    zoom = (*map_pixel(minx, miny, 800, 800, zoom), *map_pixel(maxx, maxy, 800, 800, zoom))
                    del drag_end
                    drag_start = None
                else:
                    drag_start = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEMOTION:
                if drag_start is None and tracer_julia:
                    if just_juliad:
                        continue
                    just_juliad = True
                    mx, my = map_pixel(*pygame.mouse.get_pos(), 800, 800, zoom)
                    screen.fill((0, 0, 0), (800, 0, 800, 800))
                    maximum = 1
                    y_x = [[0 for _ in range(800)] for _ in range(800)]
                    print("Started julia")
                    pts: tuple[tuple[float, float],...] = path(mx, my, 10_000_000)
                    for pt in pts:
                        screen_space = map_pixel_reverse(*pt, 800, 800, orig_zoom)
                        try:
                            y_x[screen_space[1]][screen_space[0]] += 1
                            maximum = max(maximum, y_x[screen_space[1]][screen_space[0]])
                        except IndexError:
                            pass
                    for x in range(800):
                        for y in range(800):
                            bright = round((y_x[y][x]/maximum)*255)
                            screen.set_at((x+800, y), (bright, bright, bright))
                        pygame.display.update()
                    print("Finished julia")
                else:
                    just_juliad = False
                if drag_start is not None:
                    drag_end = pygame.mouse.get_pos()
                    minx, miny = drag_start
                    maxx, maxy = drag_end
                    maxx, maxy = square(minx, miny, maxx, maxy)

                    minx_bkp = minx
                    miny_bkp = miny

                    minx, miny = min(minx, maxx), min(miny, maxy)
                    maxx, maxy = max(minx_bkp, maxx), max(miny_bkp, maxy)

                    del drag_end
                    screen.blit(screen_bkp, (0, 0))
                    pygame.draw.rect(screen, (255, 255, 255), (minx, miny, maxx-minx, maxy-miny), 3, 2)
                    pygame.display.update()
                elif zoom == orig_zoom or tracer_points:
                    # visualize path
                    mx, my = map_pixel(*pygame.mouse.get_pos(), 800, 800, zoom)
                    screen.blit(screen_bkp, (0, 0))
                    screen.fill((0, 0, 0), (800, 0, 800, 800))
                    points = [(mx, my)]
                    curr_x = mx
                    curr_y = my
                    break_next = False
                    for iters in range(500 if tracer_points else 50):
                        old_x = curr_x
                        old_y = curr_y
                        curr_x = (old_x * old_x) - (old_y * old_y)
                        curr_y = 2 * old_x * old_y

                        curr_x += mx
                        curr_y += my
                        points.append((curr_x, curr_y))
                        if break_next:
                            break
                        if absolute(curr_x, curr_y) > 2:
                            break_next = True
                    for i in range(len(points) - 1):
                        from_pt = points[i]
                        to_pt = points[i+1]

                        from_pt = map_pixel_reverse(*from_pt, 800, 800, orig_zoom if tracer_points else zoom)
                        to_pt = map_pixel_reverse(*to_pt, 800, 800, orig_zoom if tracer_points else zoom)
                        col = rainbow(i, len(points), True)
                        if break_next:
                            col = (255, 255, 255)
                        if tracer_points:
                            r = 1.5
                            c = (0, 255, 255)
                            if 0 <= from_pt[0] < 800 and 0 <= from_pt[1] < 800:
                                from_pt = (from_pt[0]+800, from_pt[1])
                                try:
                                    raise IndexError
                                    pygame.draw.circle(screen, [255 - v for v in screen.get_at(from_pt)], from_pt, r)
                                    #pygame.draw.circle(screen, (0, 0, 0), from_pt, r+2)
                                    #pygame.draw.circle(screen, (255, 255, 255), from_pt, r)
                                except IndexError:
                                    pygame.draw.circle(screen, c, from_pt, r)  # sometimes it tires drawing outside the screen
                            #try:
                            #    pygame.draw.circle(screen, [255 - v for v in screen.get_at(to_pt)], to_pt, r)
                            #except IndexError:
                            #    pygame.draw.circle(screen, c, to_pt, r)  # sometimes it tries drawing outside the screen
                            #screen.set_at(from_pt, (255, 255, 255))
                            #screen.set_at(to_pt, (255, 255, 255))
                        else:
                            pygame.draw.line(screen, col, from_pt, to_pt)
                    pygame.display.update()
            elif event.type == pygame.KEYDOWN:
                just_juliad = False
                if event.key == pygame.K_BACKSPACE and not zoom_stack.is_empty():
                    zoom = zoom_stack.remove_front()
                if event.key == pygame.K_ESCAPE and drag_start is not None:
                    screen.blit(screen_bkp, (0, 0))
                    pygame.display.update()
                    drag_start = None
                if event.key == pygame.K_SPACE:
                    use_hls = not use_hls
                    pygame.display.set_caption("Color mode: " + ("HLS" if use_hls else "HSV"), "")
                elif event.key == pygame.K_RETURN:
                    path_mode = not path_mode
                elif event.key == pygame.K_r:
                    screen.fill((255, 255, 255))
                    prev_zoom = None
                elif event.key == pygame.K_p:
                    tracer_points = not tracer_points
                elif event.key == pygame.K_j:
                    tracer_julia = not tracer_julia
                elif event.key == pygame.K_o:
                    print(f"{zoom=}")
                elif event.key == pygame.K_EQUALS: # +
                    iter_count *= 10
                    print(f"New iter count: {iter_count}")
                elif event.key == pygame.K_MINUS:  # -
                    iter_count /= 10
                    iter_count = int(iter_count)
                    if iter_count <= 0:
                        iter_count = 1
                    print(f"New iter count: {iter_count}")
            else:
                just_juliad = False
        if prev_zoom != zoom or prev_path_mode != path_mode or iter_count != old_iter_count:
            prev_zoom = zoom
            prev_path_mode = path_mode
            draw(zoom, screen, escape=iter_count)
            old_iter_count = iter_count
            screen_bkp.blit(screen, (0, 0))

        if just_juliad:
            if just_juliad_end is None:
                just_juliad_end = time.time() + 0.5
            elif just_juliad_end < time.time():
                just_juliad_end = None
                just_juliad = False

    pygame.quit()
