import colorsys
import math


avg_i = None
def draw(dim: int, pygame, screen, y_x: list[list[tuple[int, float, float]]]):
    global avg_i
    if avg_i is None:
        avg_i = 0
        avg_c = 0
        for y in range(dim):
            for x in range(dim):
                it, _, _ = y_x[y][x]
                if it != -1:
                    avg_i += it
                    avg_c += 1
        avg_i /= avg_c
    for y in range(dim):
        pygame.display.update()
        for x in range(dim):
            data = y_x[y][x]
            screen.set_at((x, y), color(*data, x, y, avg_i))
    pygame.display.update()

def _clean(c: tuple[int, int, int]) -> tuple[int, int, int]:
    # noinspection PyTypeChecker
    return tuple(max(0, min(int(n), 255)) for n in c)

def _to_255(c: tuple[float, float, float]) -> tuple[int, int, int]:
    # noinspection PyTypeChecker
    return tuple(n*255 for n in c)

# averaging colorization
def color(iters: int, fx: float, fy: float, x: int, y: int, avg_iters: float) -> tuple[int, int, int]:
    if iters == -1:
        return 0, 0, 0
    #try:
    #    return _clean(_to_255(colorsys.hls_to_rgb(math.log2(iters*iters*iters) / max(0.00001, (x*x + y*y)**2), 0.5, 1)))#fx/15+0.5)))
    #except ValueError:
    #    return 255, 0, 0
    #return _clean(_to_255(colorsys.hls_to_rgb((fx*fx + fy*fy)/15, 0.5, 1)))
    try:
        return _clean(_to_255(colorsys.hls_to_rgb(iters/avg_iters, 0.5, 1)))
    except ValueError:
        return (255, 0, 0)