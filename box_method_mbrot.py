import mbrot
import pygame
import colorsys

def _clean(c: tuple[int|float, int|float, int|float]) -> tuple[int, int, int]:
    # noinspection PyTypeChecker
    return tuple(max(0, min(int(n), 255)) for n in c)

def _to_255(c: tuple[float, float, float]) -> tuple[int, int, int]:
    # noinspection PyTypeChecker
    return tuple(n*255 for n in c)

pygame.init()

DIM = 1024

screen = pygame.display.set_mode((DIM, DIM))

def in_set(x: int, y: int):
    key = (x, y)
    if key in in_set.cache:
        return in_set.cache[key]
    mx, my = mbrot.map_pixel(x, y, DIM, DIM, (-2.5, -2, 1.5, 2))
    is_in_set = mbrot.point(mx, my, 1_000)[0] == -1
    in_set.cache[key] = is_in_set
    return is_in_set

in_set.cache: dict[tuple[int, int], bool] = {}

class Box:
    def __init__(self, rect: pygame.Rect, level: int = 0):
        self.children: list[Box] | None = None
        self.rect: pygame.Rect = rect
        self.entirely_contained = True
        self.level = level

    def mandel_calc(self):
        for x in range(self.rect.left, self.rect.right+1):
            if not in_set(x, self.rect.top) or not in_set(x, self.rect.bottom):
                self.entirely_contained = False
                break
        if self.entirely_contained:
            for y in range(self.rect.top, self.rect.bottom+1):
                if not in_set(self.rect.left, y) or not in_set(self.rect.right, y):
                    self.entirely_contained = False
                    break
        if not self.entirely_contained:
            if self.rect.width > 2 and self.rect.height > 2:
                self.split()
                for child in self.children:
                    child.mandel_calc()

    def mandel_draw(self, surf: pygame.Surface):
        # pygame.display.update()
        if self.entirely_contained:
            pygame.draw.rect(surf, _clean(_to_255(colorsys.hls_to_rgb(self.level / 8, 0.5, 1))), self.rect)
            pygame.display.update()
        elif self.children is not None:
            for child in self.children:
                child.mandel_draw(surf)
        else:
            # print("Drawing lazily")
            for x in range(self.rect.left, self.rect.right+1):
                for y in range(self.rect.top, self.rect.bottom+1):
                    if in_set(x, y):
                        surf.set_at((x, y), (0, 0, 0))
                #pygame.display.update()

    def draw(self, surf: pygame.Surface):
        pygame.draw.line(surf, (255, 255, 255), self.rect.topleft, self.rect.topright)
        pygame.draw.line(surf, (255, 255, 255), self.rect.topright, self.rect.bottomright)
        pygame.draw.line(surf, (255, 255, 255), self.rect.bottomright, self.rect.bottomleft)
        pygame.draw.line(surf, (255, 255, 255), self.rect.bottomleft, self.rect.topleft)
        if self.children is not None:
            for child in self.children:
                child.draw(surf)

    def split_at(self, click_pos: tuple[int, int]):
        if not self.rect.collidepoint(*click_pos):
            return
        if self.children is None:
            self.split()
        else:
            for child in self.children:
                child.split_at(click_pos)

    def split(self):
        if self.children is None:
            x_split = self.rect.centerx
            y_split = self.rect.centery
            """
                                    rect.top
                    |-----------------|-----------------|
                    |                 |                 |
                    |                 |                 |
                    |                 |                 |
                    |                 |     y_split     |
        rect.left   |-----------------|-----------------|   rect.right
                    |                 |                 |
                    |                 |                 |
                    |                 |x_split          |
                    |                 |                 |
                    |-----------------|-----------------|
                                    rect.bottom
    """
            self.children = [
                Box(pygame.Rect(self.rect.left, self.rect.top, x_split-self.rect.left, y_split-self.rect.top), level=self.level+1),
                Box(pygame.Rect(x_split, self.rect.top, self.rect.right-x_split, y_split-self.rect.top), level=self.level+1),
                Box(pygame.Rect(self.rect.left, y_split, x_split - self.rect.left, self.rect.bottom - y_split), level=self.level+1),
                Box(pygame.Rect(x_split, y_split, self.rect.right - x_split, self.rect.bottom - y_split), level=self.level+1)
            ]
        else:
            for child in self.children:
                child.split()

main = Box(pygame.Rect(0, 0, DIM, DIM))

calculated = False
draw_mandelbrot = False
kg = True
while kg:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            kg = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                main.split()
            elif event.key == pygame.K_RETURN:
                # main = Box(pygame.Rect(0, 0, DIM, DIM))
                if not calculated:
                    calculated = True
                    print("Calculating")
                    main.mandel_calc()
                    print("Done")
                    draw_mandelbrot = True
            elif event.key == pygame.K_m:
                draw_mandelbrot = not draw_mandelbrot
            elif event.key == pygame.K_h:
                orig_dim = DIM
                DIM = 8096
                print(f"rendering hi-res {DIM=}")
                tmp = Box(pygame.Rect(0, 0, DIM, DIM))
                print("Calculating")
                tmp.mandel_calc()
                print("Drawing")
                surf = pygame.Surface((DIM, DIM))
                surf.fill((255, 255, 255))
                tmp.mandel_draw(surf)
                print("Done drawing")
                pygame.image.save(surf, "hires.png")
                print("Saved")

                DIM = orig_dim
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mp = pygame.mouse.get_pos()
            main.split_at(mp)

    if draw_mandelbrot:
        screen.fill((255, 255, 255))
        main.mandel_draw(screen)
        pygame.display.update()
        input("press enter to redraw")
        draw_mandelbrot = False
    else:
        screen.fill((0, 0, 0))
        main.draw(screen)
    pygame.display.update()

pygame.quit()